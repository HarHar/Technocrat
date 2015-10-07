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
		<img src="/static/glyphicons/glyphicons/png/"""+ mI['icon'] + """\" />
		<div class="menuInfo"> """ + mI['text'] + """ </div>
	</div>
				"""
		except: pass

	utils.load(client, css='page.css', html='page.html', js='page.js', replaces={'$title': utils.link['mainChannel'], '$menuBar': menuBar})

def showHome(utils, client):
	utils.loadRawHTML(client, 'test :3')

def showAbout(utils, client):
	utils.loadRawHTML(client, 'placeholder')

provides = {'main': setMain, 'showHome': showHome, 'showAbout': showAbout}
menuItems = [{'id': 'home', 'icon': 'glyphicons-21-home.png', 'text': 'Home', 'module': 'main', 'method': 'showHome'},
			{'id': 'about', 'icon': 'glyphicons-196-circle-info.png', 'text': 'About us', 'module': 'main', 'method': 'showAbout'}]