if __name__ == '__main__': exit()

import traceback
import cgi
#import eventlet
import threading
import time

def telegramThread(botmodule):
	import telegram	
	import storage
	telegramBot = telegram.Bot(token=storage.db.data['telegramToken'])

	try:
		LAST_UPDATE_ID = telegramBot.getUpdates()[-1].update_id
	except IndexError:
		LAST_UPDATE_ID = None

	while True:
		time.sleep(2)
		try:
			updates = telegramBot.getUpdates(offset=LAST_UPDATE_ID)
		except:
			time.sleep(60)
			continue
		for update in updates:
			chat_id = update.message.chat_id
			message = update.message.text
			tgMsg = ''
			if (message.lower().find('!mute') == 0):
				botmodule.bot.connection.mode('#/g/technology', '+m')
				tgMsg = 'Setting mode +m on channel'
			elif (message.lower().find('!unmute') == 0):
				botmodule.bot.connection.mode('#/g/technology', '-m')
				tgMsg = 'Setting mode -m on channel'
			elif (message.lower().find('!kick') == 0):
				if len(message.lower().split(' ')) > 1:
					who = message.split(' ')[1]
				else:
					who = botmodule.bot.link['common'].get('lastReported', False)

				if who:
					tgMsg = 'Kicking ' + who
					botmodule.bot.connection.privmsg('ChanServ', 'kick #/g/technology ' + who + ' Requested by Telegram interface')
				else:
					tgMsg = 'kick who? idk'
			elif (message.lower().find('!ban') == 0):
				if len(message.lower().split(' ')) > 1:
					who = message.split(' ')[1]
				else:
					who = botmodule.bot.link['common'].get('lastReported', False)

				if who:
					tgMsg = 'Banning ' + who
					botmodule.bot.connection.privmsg('ChanServ', 'kb #/g/technology ' + who + ' Requested by Telegram interface')
				else:
					tgMsg = 'ban who? idk'
			elif (message.lower().find('!lastlines') == 0):
				try:
					if len(message.lower().split(' ')) > 1:
						if message.split(' ')[1].isdigit():
							howmuch = int(message.split(' ')[1])
						else:
							telegramBot.sendMessage(chat_id=chat_id, text='Error, second parameter must be a digit')
							LAST_UPDATE_ID = update.update_id + 1
							continue
					else:
						howmuch = 5

					towho = update.message.from_user.id

					telegramBot.sendMessage(chat_id=chat_id, text='Sending you the last ' + str(howmuch) + ' lines in private')

					for logItem in botmodule.bot.link['irc']['log'][-howmuch:]:
						if logItem['type'] == 'message':
							telegramBot.sendMessage(chat_id=towho, text='<' + logItem['source'].split('!')[0] + '> ' + logItem['message'])
					LAST_UPDATE_ID = update.update_id + 1
				except:
					telegramBot.sendMessage(chat_id=chat_id, text='Exception occured :< probably gotta wait a bit for messages to pile up')
					LAST_UPDATE_ID = update.update_id + 1
				continue

			if tgMsg:
				try:
					telegramBot.sendMessage(chat_id=chat_id, text=tgMsg)
				except:
					print('error sending message [telegram]')		
			LAST_UPDATE_ID = update.update_id + 1


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
	m = BotModule()
	t = threading.Thread(target=telegramThread, args=(m,))
	t.setDaemon(True)
	t.start()
	return {'name': 'peeking module', 'object': m}