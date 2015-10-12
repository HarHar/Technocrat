import glob
import random

def setMain(utils, client):
	#utils.loadCSS(client, 'page.css')
	#utils.loadHTML(client, 'page.html', {'$title': '#/g/technology'})
	#utils.loadJS(client, 'page.js')

	menuBar = ''
	for module in utils.modules.webmodules:
		try:
			for menuItem in module.web.menuItems:
				mI = menuItem
				aux = 'selected' if mI['id'] == 'home' else ''
				menuBar += """
	<div id=\"""" + mI['id'] + """\" class="menuItem """ + aux + """\" module=\"""" + mI['module'] + """\" method=\"""" + mI['method'] + """\">
		<img src="/static/glyphicons/glyphicons/png/""" + mI['icon'] + """\" />
		<div class="menuInfo"> """ + mI['text'] + """ </div>
	</div>
				"""
		except: pass

	mascot = '/' + random.choice(glob.glob('static/mascots/*'))
	utils.load(client, css='page.css', html='page.html', js='page.js', replaces={'$title': utils.link['mainChannel'], '$menuBar': menuBar, '$mascot': mascot})

def showHome(utils, client):
	chan = utils.link['irc']['bot'].channels[utils.link['mainChannel']]

	users = chan.users()
	usersNumber = len(users)
	mods = sorted(list(chan.owners())) + sorted(list(chan.opers())) + sorted(list(chan.halfops()))
	opers = '<br />'.join([('<span style="color: #AE0000; margin-left: 50px;">' + x + '</span>') for x in mods])
	voices = '<br />'.join([('<span style="color: #9E7B00; margin-left: 50px;">' + x + '</span>') for x in sorted(list(chan.voiced()))])
	lastSpoke = '<br />'.join([('<span style="color: #75507B; margin-left: 50px;">' + x + '</span>') for x in utils.link['irc']['bot'].lastSpoke][::-1])

	out = 'We currently have <span class="bigger green">' + str(usersNumber) + '</span> online users<br />'
	out += '<div style="float: left; width: 200px; padding: 20px; border: 1px solid #9E7B00; margin: 10px;">Our most esteemed online members are: ' + voices + '</div>'
	out += '<div style="float: left; width: 200px; padding: 20px; border: 1px solid #AE0000; margin: 10px;">Our currently online mods are: ' + opers + '</div>'
	out += '<div style="float: left; width: 200px; padding: 20px; border: 1px solid #75507B; margin: 10px;">Last 10 users that spoke: <br />' + lastSpoke + '</div>'

	rules = ['No ponies, fur, pepe or shitposting', 'Keep the discussions civil, this isn\'t a brothel.', 'All bots are dissallowed from the channel unless explicitly defined by Zanthas, this is to disallow spam and confusion between bots.', 'Rules and punishment are at the discretion of the moderation Team (HOP and higher)']
	fRules = ''.join([('<span style="color: #FFF">#' + str(i+1) + '</span> ' + x + '<br /><br />') for i, x in enumerate(rules)])

	out += '<br /><br />'
	out += '<div style="float: left; min-width: 200px; max-width: 500px; padding: 20px; background-color: #AE0000; margin: 10px; color: #DDD; font-weight: bold; font-size: 24px;">Now for our rules: <br />' + fRules + '</div>'

	utils.loadRawHTML(client, out)

def showAbout(utils, client):
	history = """In early 2012 one of the current owners, dissatisfied with the /g/ channels that existed, sought to create a different one. One that was actually about technology. He posted on /g/ about his desire to create a new channel, and invited others to join him. He then invited his friends from former software projects and #/g/technology was born.
<br /><br />The channel has grown a lot since then, it was considered the de-facto /g/ channel and was by far the largest channel for 4chan's technology board, but recently we have become more than just a 4chan related channel, and have embraced people from across the web. <br /> <br /> <span style="color: #AE0000">We hope to continue this growth so that we can become the defacto irc channel for all technology related discussion.</span>"""

	out = 'Our IRC channel, <span class="blue">#/g/technology</span>, currently lives on <span class="blue">Rizon</span> (irc.rizon.net:6667).<br />Now here\'s the story of our channel:<br /><br />'
	out += history
	out += '<br /><br />'
	out += '<span class="bigger green">&gt;4chan<br/>&gt;2015</span>'
	utils.loadRawHTML(client, out)

def getNewMascot(utils, client):
	mascot = '/' + random.choice(glob.glob('static/mascots/*'))
	client.emit('setMascot', mascot, room=utils.sid)

provides = {'main': setMain, 'showHome': showHome, 'showAbout': showAbout, 'getNewMascot': getNewMascot}
menuItems = [{'id': 'home', 'icon': 'glyphicons-21-home.png', 'text': 'Home', 'module': 'main', 'method': 'showHome'},
			{'id': 'about', 'icon': 'glyphicons-196-circle-info.png', 'text': 'About us', 'module': 'main', 'method': 'showAbout'}]