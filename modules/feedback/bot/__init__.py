if __name__ == '__main__': exit()

import traceback
import cgi
import threading
import time

class BotModule(object):
	def __init__(self):
		pass
	def onMessage(self, message, source, target):
		if self.bot.link['irc'].get('log', None) is None:
			self.bot.link['irc']['log'] = []
		self.bot.link['irc']['log'].append({'type': 'message', 'target': target, 'source': source, 'message': message})

		if target != self.bot.link['mainChannel']: return
		out = '<chatItem>'
		nick = source.split('!')[0]
		message = cgi.escape(message)

		op = False
		voice = False
		chan = self.bot.channels[self.bot.link['mainChannel']]
		if chan.is_halfop(nick) or chan.is_oper(nick) or chan.is_owner(nick):
			op = True
		if chan.is_voiced(nick):
			voice = True

		if op:
			out += '&lt;<span style="color: #AE0000;">' + nick + '</span>&gt; ' + message
		elif voice:
			out += '&lt;<span style="color: #9E7B00;">' + nick + '</span>&gt; ' + message
		else:
			out += '&lt;' + nick + '&gt; ' + message

		out += '<br />'
		out += '</chatItem>'

		#self.bot.link['web']['sio'].emit('logMessage', out)
		try:
			self.bot.link['broadcast'].append(['logMessage', (out,)])
		except: pass

def getModule():
	return {'name': 'feedback module', 'object': BotModule()}