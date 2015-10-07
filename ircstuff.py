#!/usr/bin/env python
# -*- encoding: utf8 -*-
import sys
sys.dont_write_bytecode = True
import traceback

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr

import storage
import modules

class TechBot(irc.bot.SingleServerIRCBot):
	# cheat sheet
	# self.disconnect -> disconnects
	# self.die() -> dies
	# e -> event??
	# self.connection -> c
	# c.notice(nick, msg)
	# self.channels -> list of channel objects

	def __init__(self, link, channel, nickname, server, password='', port=6667):
		irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
		self.link = link
		self.link['irc']['bot'] = self
		self.password = password


		self.channel = channel
		self.modules = {}
		self.printLogs = False
		for module in modules.ircmodules:
			modInfo = module.bot.getModule()
			modInfo['object'].bot = self
			modInfo['object'].conn = self.connection
			modInfo['storage'] = storage
			self.modules[modInfo['name']] = modInfo

	def log(self, msg):
		if self.printLogs:
			print(msg)

	def on_passwdmismatch(self, *args):
		if self.password:
			self.connection.pass_(self.password)

	def callModules(self, command, params):
		for module in self.modules:
			self.log('[call] ' + module + '.' + command + '(' + repr(params) + ')')
			try:
				getattr(self.modules[module]['object'], command)(*params)
			except:
				self.log('[call error] on ' + module + '.' + command + '(' + repr(params) + ')')
				traceback.print_exc()
			else:
				self.log('[call return] ' + module + '.' + command + '(' + repr(params) + ')')

	def on_nicknameinuse(self, c, e):
		c.nick('_' + c.get_nickname() + '_')

	def on_welcome(self, c, e):
		c.join(self.channel)

	def on_privmsg(self, c, e):
		self.do_command(e, e.arguments[0])

	def on_pubmsg(self, c, e):
		message = e.arguments[0]
		source = e.source
		target = e.target
		connection = self.connection

		self.callModules('onMessage', (message, source, target))

		#a = e.arguments[0].split(":", 1)
		#if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(self.connection.get_nickname()):
		#	self.do_command(e, a[1].strip())
		#return

	def on_dccmsg(self, c, e):
		# non-chat DCC messages are raw bytes; decode as text
		text = e.arguments[0].decode('utf-8')
		c.privmsg("You said: " + text)

	def on_dccchat(self, c, e):
		if len(e.arguments) != 2:
			return
		args = e.arguments[1].split()
		if len(args) == 4:
			try:
				address = ip_numstr_to_quad(args[2])
				port = int(args[3])
			except ValueError:
				return
			self.dcc_connect(address, port)

	#def do_command(self, e, cmd):
	#nick = e.source.nick
	#c = self.connection

	#if cmd == "disconnect":
	#	self.disconnect()
	#elif cmd == "die":
	#	self.die()
	#elif cmd == "stats":
	#	for chname, chobj in self.channels.items():
	#		c.notice(nick, "--- Channel statistics ---")
	#		c.notice(nick, "Channel: " + chname)
	#		users = sorted(chobj.users())
	#		c.notice(nick, "Users: " + ", ".join(users))
	#		opers = sorted(chobj.opers())
	#		c.notice(nick, "Opers: " + ", ".join(opers))
	#		voiced = sorted(chobj.voiced())
	#		c.notice(nick, "Voiced: " + ", ".join(voiced))
	#elif cmd == "dcc":
	#	dcc = self.dcc_listen()
	#	c.ctcp("DCC", nick, "CHAT chat %s %d" % (
	#		ip_quad_to_numstr(dcc.localaddress),
	#		dcc.localport))
	#else:
	#	c.notice(nick, "Not understood: " + cmd)

def main(link):
	channel = storage.db.data['ircbotchannel']
	mainChannel = storage.db.data['ircchannel']
	nickname = storage.db.data['ircnick']
	server = storage.db.data['irchost']
	port = storage.db.data['ircport']
	password = storage.db.data['ircpassword']

	link['mainChannel'] = mainChannel
	bot = TechBot(link, channel, nickname, server, port=port, password=password)
	bot.start()

if __name__ == "__main__":
	exit()