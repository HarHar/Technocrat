def showFeedback(utils, client):
	loggedIn = False
	unick = ''
	for nick in utils.link['common']['loggedUsers']:
		if utils.link['common']['loggedUsers'][nick] == utils.sid:
			loggedIn = True
			unick = nick
	chan = utils.link['irc']['bot'].channels[utils.link['mainChannel']]

	out = '<span class="green" style="font-size: 42px">Feedback/suggestions box</span><br />'
	if loggedIn:
		out += '<span style="color: #BBB;">Your feedback will be signed as <b>&lt;' + unick + '&gt;</b></span><br /><br />'
	else:
		out += '<span style="color: #BBB;">Your feedback will be signed as <b>&lt;anonymous&gt;</b><br/>We might not be able to respond, click <a href="" onclick="return false;" id="goLogin">here</a> to login</span><br /><br />'
	out += '<textarea rows="10" cols="50" id="feedbackText">Write your feedback here</textarea><br />'
	out += '<input type="button" id="feedbackSubmit" value="submit" />'
	utils.loadCSS(client, 'page.css')
	utils.loadRawHTML(client, out)
	utils.loadJS(client, 'page.js')

def submitFeedback(utils, client, fback):
	fromNick = '<anonymous>'
	for nick in utils.link['common']['loggedUsers']:
		if utils.link['common']['loggedUsers'][nick] == utils.sid:
			fromNick = nick
			break

	bot = utils.link['irc']['bot']
	chan = bot.channels[utils.link['mainChannel']]
	testChan = bot.channels[utils.link['storage'].db.data['ircbotchannel']]

	messages = [chr(2) + chr(3) + '7[feedback]' + chr(15)]
	messages.append('FROM: ' + fromNick)

	fback = fback.replace('\r', '').split('\n')
	messages += fback

	for message in messages:
		utils.link['irc']['bot'].connection.privmsg(utils.link['storage'].db.data['ircbotchannel'], message)

	utils.loadRawHTML(client, '<span class="green" style="font-size: 72px">Feedback submited!</span>')

provides = {'showFeedback': showFeedback, 'submitFeedback': submitFeedback}
menuItems = [{'id': 'feedback', 'icon': 'glyphicons-490-handshake.png', 'text': 'Feedback', 'module': 'feedback', 'method': 'showFeedback'}]