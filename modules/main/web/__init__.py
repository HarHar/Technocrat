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

	utils.load(client, css='page.css', html='page.html', js='page.js', replaces={'$title': utils.link['mainChannel'], '$menuBar': menuBar})

def showHome(utils, client):
	history = """In early 2012 one of the current owners, dissatisfied with the /g/ channels that existed, sought to create a different one. One that was actually about technology. He posted on /g/ about his desire to create a new channel, and invited others to join him. He then invited his friends from former software projects and #/g/technology was born.
The channel has grown a lot since then, and is now considered the de-facto /g/ channel and is by far the largest channel for 4chan's technology board. """

	chan = utils.link['irc']['bot'].channels[utils.link['mainChannel']]

	users = chan.users()
	usersNumber = len(users)
	mods = sorted(list(chan.owners())) + sorted(list(chan.opers())) + sorted(list(chan.halfops()))
	opers = '<br />'.join([('<span style="color: #AE0000; margin-left: 50px;">' + x + '</span>') for x in mods])
	voices = '<br />'.join([('<span style="color: #9E7B00; margin-left: 50px;">' + x + '</span>') for x in sorted(list(chan.voiced()))])

	out = 'We currently have <span class="bigger green">' + str(usersNumber) + '</span> online users<br />'
	out += '<div style="float: left; width: 200px; padding: 20px; border: 1px solid #AE0000; margin: 10px;">Our currently online mods are: ' + opers + '</div>'
	out += '<div style="float: left; width: 200px; padding: 20px; border: 1px solid #9E7B00; margin: 10px;">Our most steemed online members are: ' + voices + '<br />'

	utils.loadRawHTML(client, out)

def showAbout(utils, client):
	utils.loadRawHTML(client, 'placeholder')

provides = {'main': setMain, 'showHome': showHome, 'showAbout': showAbout}
menuItems = [{'id': 'home', 'icon': 'glyphicons-21-home.png', 'text': 'Home', 'module': 'main', 'method': 'showHome'},
			{'id': 'about', 'icon': 'glyphicons-196-circle-info.png', 'text': 'About us', 'module': 'main', 'method': 'showAbout'}]