def setMain(utils, client):
	utils.loadCSS(client, 'page.css')
	utils.loadJS(client, 'page.js')
	utils.loadHTML(client, 'page.html')

provides = {'main': setMain}