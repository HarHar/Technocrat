var ayy = true;

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

var spinner = '<div class="spinner"> <div class="rect1"></div> <div class="rect2"></div> <div class="rect3"></div> <div class="rect4"></div> <div class="rect5"></div> </div>'

$('.menuItem').click(function() {
	$this = $(this);
	$('.menuItem.selected').removeClass('selected');
	$this.addClass('selected');

	toggleHeaderEffect();
	$('#realContent').html(spinner);
	socket.emit('callModule', $this.attr('module'), $this.attr('method'));
});

socket.on('setModuleContent', function(html) {
	$('#realContent').html(html);
});

socket.emit('callModule', 'main', 'showHome');