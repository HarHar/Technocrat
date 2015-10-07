def setMain(utils, client):
	#utils.loadCSS(client, 'page.css')
	#utils.loadHTML(client, 'page.html', {'$title': '#/g/technology'})
	#utils.loadJS(client, 'page.js')
	utils.load(client, css='page.css', html='page.html', js='page.js', replaces={'$title': '#/g/technology'})

def test(utils, client):
	utils.loadRawHTML(client, 'test :3')

provides = {'main': setMain, 'test': test}