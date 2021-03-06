#!/usr/bin/env python2
# -*- encoding: utf8 -*-
import sys
sys.dont_write_bytecode = True

import eventlet
import os
import sys
from flask import Flask, render_template, request, redirect, session, Response
import socketio
import threading
import time
import json
import subprocess

import modules

fapp = Flask(__name__)
sio = socketio.Server()

class utilities(object):
	def __init__(self):
		self.sid = None
		self.sio = None
		self.modulePath = ''
		self.link = {}
		self.modules = None
		self.submodule = False
	def staticFilePath(self, f, aux=False):
		if f[-3:] in ['css', '.js']:
			URLMod = '_' if aux else ''
			return '/' + URLMod + 'getstatic/' + os.path.join(self.modulePath, f)
	def readFile(self, path):
		f = open(os.path.join(self.modulePath, path), 'r')
		data = f.read()
		f.close()
		return data
	def loadJS(self, sio, filename, aux=False):
		if self.submodule:
			sio.emit('loadModuleJS', self.staticFilePath(filename, aux), room=self.sid)
		else:
			sio.emit('loadJS', self.staticFilePath(filename, aux), room=self.sid)
	def loadCSS(self, sio, filename):
		if self.submodule:
			sio.emit('loadModuleCSS', self.staticFilePath(filename), room=self.sid)
		else:
			sio.emit('loadCSS', self.staticFilePath(filename), room=self.sid)
	def loadRawHTML(self, sio, html):
		if self.submodule:
			sio.emit('setModuleContent', html, room=self.sid)
		else:
			sio.emit('setContent', html, room=self.sid)
	def loadHTML(self, sio, filename, replaces={}):
		content = self.readFile(filename)
		for key in replaces:
			content = content.replace(key, replaces[key])
		if self.submodule:
			sio.emit('setModuleContent', content, room=self.sid)
		else:
			sio.emit('setContent', content, room=self.sid)
	def load(self, sio, html='', css='', js='', replaces={}):
		if css:
			self.loadCSS(sio, css)
		if html and css:
			content = self.readFile(html)
			for key in replaces:
				content = content.replace(key, replaces[key])

			content += """
				<script>
					if (window.entryPoint === undefined) {
						window.needEntry = false
					} else {
						window.entryPoint();
						window.entryPoint = undefined;
					}
				</script>
			"""

			if self.submodule:
				sio.emit('setModuleContent', content, room=self.sid)
				sio.emit('loadModuleJS', self.staticFilePath(js, aux=True), room=self.sid)
			else:
				sio.emit('setContent', content, room=self.sid)
				sio.emit('loadJS', self.staticFilePath(js, aux=True), room=self.sid)
		else:
			if html:
				self.loadHTML(sio, html, replaces)

globalUtils = utilities()

@fapp.route('/')
def getLoader():
	return render_template('loader.html')

@fapp.route('/main')
def getMain():
	return render_template('main.html')

@fapp.route('/getstatic/<path:p>')
def getStatic(p):
	if ('..' in p) or (p.find('static') != -1) or (p.startswith('modules/') == False) or (p.find('/web/') == -1):
		return
	mimetype = 'text/css' if p.endswith('.css') else 'application/javascript'
	return Response(globalUtils.readFile(p), mimetype=mimetype)

@fapp.route('/_getstatic/<path:p>')
def getStatic_jsmod(p):
	if ('..' in p) or (p.find('static') != -1) or (p.startswith('modules/') == False) or (p.find('/web/') == -1):
		return
	mimetype = 'text/css' if p.endswith('.css') else 'application/javascript'
	out = """
	myFunc = function() {
	""" + globalUtils.readFile(p) + """
	window.needEntry = true;
	window.entryPoint = undefined;
	}

	if (window.needEntry) {
		window.entryPoint = myFunc
	} else {
		myFunc();
	}
	"""
	return Response(out, mimetype=mimetype)

@sio.on('getContent')
def getContent(sid, which):
	for module in modules.webmodules:
		if which in module.web.provides:
			utils = utilities()
			utils.sid = sid
			utils.modulePath = module.__name__.replace('.', '/') + '/web/'
			utils.link = globalUtils.link
			utils.submodule = False
			utils.modules = modules
			module.web.provides[which](utils, sio)

@sio.on('callModule')
def callModule(sid, moduleName, methodName, *args):
	#print('[call] ' + moduleName + '.' + methodName)
	for module in modules.webmodules:
		#print('__name__ == ' + module.__name__)
		if module.__name__.split('.')[1] == moduleName:
			#print('provides = ' + repr(module.web.provides))
			if methodName in module.web.provides:
				#print('good...')
				utils = utilities()
				utils.sid = sid
				utils.submodule = True
				utils.modulePath = module.__name__.replace('.', '/') + '/web/'
				utils.modules = modules
				utils.link = globalUtils.link
				module.web.provides[methodName](utils, sio, *args)
				return
	sio.emit('setModuleContent', '<h1><font color="red">Error! Module or function not found</font></h1>')

fapp.debug = True
fapp.config['SECRET_KEY'] = 'hunter2'

def broadcastQueue(x):
	q, sio = x
	while True:
		eventlet.greenthread.sleep(1)
		for event in q:
			if len(event) == 2:
				sio.emit(event[0], *event[1])
			elif len(event) == 3:
				sio.emit(event[0], event[1], room=event[2])
			q.remove(event)

def main(link):
	app = socketio.Middleware(sio, fapp)
	fapp.link = link
	app.link = link
	globalUtils.link = link
	link['web']['sio'] = sio

	link['common']['registrationQ'] = {}
	link['common']['registrationQ2'] = {}
	link['common']['loggedUsers'] = {}

	link['broadcast'] = []
	eventlet.greenthread.spawn(broadcastQueue, (link['broadcast'], sio))

	eventlet.wsgi.server(eventlet.listen(('', link['storage'].db.data['webport'])), app)

if __name__ == '__main__':
	exit()