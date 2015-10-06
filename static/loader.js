//returns unix timestamp
Date.now = function() { return new Date().getTime(); }

//dynamic external file loaders
//from http://stackoverflow.com/questions/9979415/dynamically-load-and-unload-stylesheets
function loadjscssfile(filename, filetype){
	filename = filename + '?' + Date.now().toString()
    if (filetype=="js"){
        var fileref=document.createElement('script')
        fileref.setAttribute("type","text/javascript")
        fileref.setAttribute("src", filename)
    }
    else if (filetype=="css"){
        var fileref=document.createElement("link")
        fileref.setAttribute("rel", "stylesheet")
        fileref.setAttribute("type", "text/css")
        fileref.setAttribute("href", filename)
    }
    if (typeof fileref!="undefined")
        document.getElementsByTagName("head")[0].appendChild(fileref)
}

function removejscssfile(filename, filetype){
    var targetelement=(filetype=="js")? "script" : (filetype=="css")? "link" : "none" //determine element type to create nodelist from
    var targetattr=(filetype=="js")? "src" : (filetype=="css")? "href" : "none" //determine corresponding attribute to test for
    var allsuspects=document.getElementsByTagName(targetelement)
    for (var i=allsuspects.length; i>=0; i--){ //search backwards within nodelist for matching elements to remove
    if (allsuspects[i] && allsuspects[i].getAttribute(targetattr)!=null && allsuspects[i].getAttribute(targetattr).indexOf(filename)!=-1)
        allsuspects[i].parentNode.removeChild(allsuspects[i]) //remove element by calling parentNode.removeChild()
    }
}

//$(document).ready(function() {
// ^ no need for this when our script is the last thing on the page

var socket = io();
$(window).on('beforeunload', function(){
    socket.close();
});

document.loadedJS = '';
document.loadedCSS = '';

socket.on('loadCSS', function(url) {
	if(document.loadedCSS.length > 0) {
		removejscssfile(document.loadedCSS, 'css');
	}
	loadjscssfile(url, 'css');
	document.loadedCSS = url;
});

socket.on('loadJS', function(url) {
	if(document.loadedJS.length > 0) {
		removejscssfile(document.loadedJS, 'js');
	}
	loadjscssfile(url, 'js');
	document.loadedJS = url;
});

socket.on('setContent', function(html) {
	setTimeout(function() {
		$('#spinner').fadeOut(1000, function() {
			$('#content').html(html);
			$('#content').fadeIn(1000);
		});
	}, 2000);
});

socket.emit('getContent', 'main');
//});