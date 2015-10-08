import cgi

def showPeek(utils, client):
	if utils.link['irc'].get('log', None) is None:
		log = []
	else:
		log = utils.link['irc']['log']

	out = '<div id="peekChat">'
	out += '<span class="bigger blue">Last 10 lines from our channel:</span><br />'
	out += '<span class="green" style="font-size: 14px;">You can join us by pointing your IRC client to #/g/technology@irc.rizon.net or clicking <a href="https://qchat.rizon.net/?randomnick=1&channels=/g/technology&uio=d4" target="_BLANK">here</a></span>'
	out += '<br /> <br />'
	for logItem in log[-10:]:
		if logItem['target'] == utils.link['mainChannel']:
			if logItem['type'] == 'message':
				out += '<chatItem>'
				nick = logItem['source'].split('!')[0]
				message = cgi.escape(logItem['message'])

				op = False
				voice = False
				chan = utils.link['irc']['bot'].channels[utils.link['mainChannel']]
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
	out += '</div>'
	out += '<br />'
	out += '<span style="color: #BBB; font-size: 12px">Updates automatically; joins/parts/quits not shown</span>'

	utils.loadCSS(client, 'page.css')
	utils.loadRawHTML(client, out)
	utils.loadJS(client, 'page.js')

provides = {'showPeek': showPeek}
menuItems = [{'id': 'peek', 'icon': 'glyphicons-52-eye-open.png', 'text': 'Take a peek', 'module': 'peek', 'method': 'showPeek'}]