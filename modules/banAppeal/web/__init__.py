def showAppealPage(utils, client):
	loggedIn = False
	unick = ''
	for nick in utils.link['common']['loggedUsers']:
		if utils.link['common']['loggedUsers'][nick] == utils.sid:
			loggedIn = True
			unick = nick
	chan = utils.link['irc']['bot'].channels[utils.link['mainChannel']]
	if not loggedIn:
		out = '<span style="color: #F00; font-weight: bold; font-size: 32px">'
		out += 'You need to be logged in to appeal a ban! ;&lt;</span>'
		utils.loadRawHTML(client, out)
		return

	out = '<span style="color: #F00; font-weight: bold; font-size: 32px">Ban appealing</span>'

	out += '<br /><br />'

	out += '<textarea rows="15" cols="50" id="appealArea">Write your ban appeal here\n'
	out += '\nQUICK TIPS:\n#1 appealing a rightfully issued ban right after it was done will most likely result in your appeal getting ignored, wait a bit mate'
	out += '\n#2 We might have banned you because you did something against the rules or because your behavior was not conducive to the desired environment'
	out += '\n#3 Do not directly PM the mods, this ban appeal _will_ get to our ears'
	out += '\n#4 Waiting is key'
	out += '\n#5 Include the ban mask on your appeal if you know it'
	out += '\n#6 Details on the report status (approval/denial/other) will get sent directly to you on IRC by one of our mods or MemoServ (if you\'re offline)'
	out += '\n#7 Further action on your part might be required by us, depending on your situation'
	out += '</textarea><br />'
	out += '<input type="button" id="appealSubmit" value="submit appeal" />'
	utils.loadCSS(client, 'page.css')
	utils.loadRawHTML(client, out)
	utils.loadJS(client, 'page.js')

def submitAppeal(utils, client, appeal):
	for nick in utils.link['common']['loggedUsers']:
		if utils.link['common']['loggedUsers'][nick] == utils.sid:
			fromNick = nick
			break
	else: return

	bot = utils.link['irc']['bot']
	chan = bot.channels[utils.link['mainChannel']]
	testChan = bot.channels[utils.link['storage'].db.data['ircbotchannel']]

	messages = [chr(2) + chr(3) + '4[!ban appeal!]' + chr(15)]
	messages.append('FROM: ' + fromNick)

	appeal = appeal.replace('\r', '').split('\n')
	messages += appeal

	for message in messages:
		utils.link['irc']['bot'].connection.privmsg(utils.link['storage'].db.data['ircbotchannel'], message)

	utils.loadRawHTML(client, '<span style="font-size: 52px">Appeal submitted, ' + fromNick + ', we hope you\'re able to get unbanned and will stay away from your ~evil~ deeds from then on</span>')

provides = {'showAppealPage': showAppealPage, 'submitAppeal': submitAppeal}
menuItems = [{'id': 'banAppeal', 'icon': 'glyphicons-521-user-ban.png', 'text': 'Ban appeal', 'module': 'banAppeal', 'method': 'showAppealPage'}]