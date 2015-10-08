def showReport(utils, client):
	chan = utils.link['irc']['bot'].channels[utils.link['mainChannel']]
	users = sorted(list(chan.users()))

	out = '<span style="color: #AE0000; font-size: 42px">Reporting</span><br /><br />'
	out += '<input type="text" name="userName" id="userName" list="userList" placeholder="Report which user?" /><datalist id="userList">'
	for user in users:
		out += '<option value="' + user + '">' + user + '</option>'
	out += '</datalist>'
	out += '<br />'
	out += '<input type="text" name="reason" id="reason" placeholder="What did this user do wrong?" /><br />'
	out += '<input type="button" id="reportSubmit" value="submit report" />'
	utils.loadCSS(client, 'page.css')
	utils.loadRawHTML(client, out)
	utils.loadJS(client, 'page.js')

def submitReport(utils, client, username, reason):
	bot = utils.link['irc']['bot']
	chan = bot.channels[utils.link['mainChannel']]
	testChan = bot.channels[utils.link['storage'].db.data['ircbotchannel']]

	messages = [chr(2) + chr(3) + '4[REPORT]' + chr(15)]
	messages.append('FROM: <unknown> ' + chr(3) + '1,1until someone teaches me how to get ip from socketio')

	if chan.has_user(username):
		messages.append('USER: ' + username + ' (found on channel)')
	else:
		messages.append('USER: ' + username + ' (not found on channel)')
	messages.append('REASON: ' + reason)

	for message in messages:
		utils.link['irc']['bot'].connection.privmsg(utils.link['storage'].db.data['ircbotchannel'], message)

	utils.loadRawHTML(client, '<span style="color: #AE0000; font-size: 72px">Report submited!!</span>')

provides = {'showReport': showReport, 'submitReport': submitReport}
menuItems = [{'id': 'report', 'icon': 'glyphicons-505-alert.png', 'text': 'Report', 'module': 'report', 'method': 'showReport'}]