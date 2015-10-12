var ayy = true;

document.loadedModuleJS = '';
document.loadedModuleCSS = '';

socket.on('loadModuleCSS', function(url) {
    if(document.loadedModuleCSS.length > 0) {
        removejscssfile(document.loadedModuleCSS, 'css');
    }
    loadjscssfile(url, 'css');
    document.loadedModuleCSS = url;
});

socket.on('loadModuleJS', function(url) {
    if(document.loadedModuleJS.length > 0) {
        removejscssfile(document.loadedModuleJS, 'js');
    }
    loadjscssfile(url, 'js');
    document.loadedModuleJS = url;
});

function toggleHeaderEffect() {
	if (ayy) {
		$('#effect').removeClass('reverseCoolAnimation');
		$('#effect').addClass('coolAnimation');
		ayy = false;
	} else {
		$('#effect').addClass('reverseCoolAnimation');
		$('#effect').removeClass('coolAnimation');
		ayy = true;
	}
}

window.toggleHeaderEffect = toggleHeaderEffect;

var spinner = '<div class="spinner"> <div class="rect1"></div> <div class="rect2"></div> <div class="rect3"></div> <div class="rect4"></div> <div class="rect5"></div> </div>'

$('.menuItem').click(function() {
	$this = $(this);
	$('.menuItem.selected').removeClass('selected');
	$this.addClass('selected');

	toggleHeaderEffect();
	$('#realContent').html(spinner);
	socket.emit('callModule', $this.attr('module'), $this.attr('method'));
});



var changingMascot;

$('#mascot').click(function() {
	if (!changingMascot) {
		changingMascot = true;
		$('#mascot').css('opacity', '0.3');
		socket.emit('callModule', 'main', 'getNewMascot');
	}
});

$('#mascot').load(function() {
	changingMascot = false;
    $('#mascot').css('opacity', '1');
});

socket.on('setMascot', function(url) {
	$('#mascot').attr('src', url);
});

socket.on('setModuleContent', function(html) {
	$('#realContent').html(html);
});

socket.emit('callModule', 'main', 'showHome');