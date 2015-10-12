import cgi

def showAccess(utils, client):
	for nick in utils.link['common']['loggedUsers']:
		if utils.link['common']['loggedUsers'][nick] == utils.sid:
			utils.loadRawHTML(client, '<span class="bigger green">You are already logged in, ' + nick + '</span>')
			return
	utils.load(client, html='page.html', css='page.css', js='page.js')

def doLogin(utils, client, nick):
	utils.link['common']['registrationQ'][nick] = utils.sid

	bot = utils.link['irc']['bot']
	bot.connection.privmsg('NickServ', 'info ' + nick)

provides = {'showAccess': showAccess, 'doLogin': doLogin}
menuItems = [{'id': 'access', 'icon': 'glyphicons-387-log-in.png', 'text': 'Log in', 'module': 'access', 'method': 'showAccess'}]