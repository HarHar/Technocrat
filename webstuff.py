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

import storage
import modules

fapp = Flask(__name__)
sio = socketio.Server()

class utilities(object):
	def __init__(self):
		self.sid = None
		self.sio = None
		self.modulePath = ''
	def staticFilePath(self, f):
		if f[-3:] in ['css', '.js']:
			return '/getstatic/' + os.path.join(self.modulePath, f)
	def readFile(self, path):
		f = open(os.path.join(self.modulePath, path), 'r')
		data = f.read()
		f.close()
		return data
	def loadJS(self, sio, filename):
		sio.emit('loadJS', self.staticFilePath(filename))
	def loadCSS(self, sio, filename):
		sio.emit('loadCSS', self.staticFilePath(filename))
	def loadHTML(self, sio, filename):
		sio.emit('setContent', self.readFile(filename))
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

@sio.on('getContent')
def getContent(sid, which):
	for module in modules.webmodules:
		if which in module.web.provides:
			utils = utilities()
			utils.sid = sid
			utils.modulePath = module.__name__.replace('.', '/') + '/web/'
			module.web.provides[which](utils, sio)

fapp.debug = True
fapp.config['SECRET_KEY'] = 'hunter2'
if __name__ == '__main__':
	app = socketio.Middleware(sio, fapp)
	eventlet.wsgi.server(eventlet.listen(('', 80)), app)

