import time

class BotModule(object):
	def __init__(self):
		self.currentNick = None #current nick nickserv is talking about
		self.notRegd = '<span class="bigger" style="color: #AE0000">Error! That nick is not registered on Rizon\'s NickServ</span>'
		self.notRegd += '<br />To register, check out <a href="https://wiki.rizon.net/index.php?title=Register_your_nickname" target="_BLANK">this page</a>'

		self.notAuthd = '<span class="bigger" style="color: #AE0000">Error! That nick is not authenticated on NickServ!</span>'

		self.ok = '<span class="bigger green">Success! You are now logged in $nick'
	def onPrivNotice(self, message, source):
		link = self.bot.link
		if link['common'].get('registrationQ2', None) is None:
			link['common']['registrationQ2'] = {}
		if link['common'].get('registrationQ', None) is None:
			link['common']['registrationQ'] = {}

		if source.split('!')[0].lower() == 'nickserv':
			for user in link['common']['registrationQ']:
				if (message.lower().find(user.lower() + ' is ') == 0) and (message.lower().find('currently online') == -1):
					self.currentNick = user
					return

				if message.lower().find('nick ' + user.lower() + ' isn\'t registered') == 0:
					link['broadcast'].append(['setModuleContent', self.notRegd, link['common']['registrationQ'].pop(user)])
					self.currentNick = None
					return

				if (self.currentNick is None) == False:
					message = message.strip().strip('\t')
					if message.lower().find('last seen time: ') == 0:
						link['broadcast'].append(['setModuleContent', self.notAuthd, link['common']['registrationQ'].pop(user)])
						self.currentNick = None
						return
					elif (message.lower().find('is online from: ') == 0) or (message.lower().find(self.currentNick.lower() + ' is currently online') == 0):
						#link['broadcast'].append('setModuleContent', (self.ok), link['common']['registrationQ'].pop(user))

						link['common']['registrationQ2'][user.lower()] = link['common']['registrationQ'].pop(user).lower()
						self.bot.connection.privmsg(user, 'You have requested a login on #/g/technology\'s website')
						self.bot.connection.privmsg(user, 'Reply me with "confirm login" to accept the login request')
						self.bot.connection.privmsg(user, 'If you did not request this, please ignore this message.')
						self.currentNick = None
						return
	def onPrivMessage(self, message, source):
		link = self.bot.link
		if source.split('!')[0].lower() in link['common']['registrationQ2']:
			if message.lower().strip() == 'confirm login':
				sid = link['common']['registrationQ2'].pop(source.split('!')[0].lower())
				link['common']['loggedUsers'][source.split('!')[0].lower()] = sid
				link['broadcast'].append(['setModuleContent', self.ok.replace('$nick', source), sid])
				self.bot.connection.privmsg(source.split('!')[0], chr(3) + '3OK! Login accepted')

def getModule():
	return {'name': 'login module', 'object': BotModule()}