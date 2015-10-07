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

$('.menuItem').click(function() {
	$this = $(this);
	$('.menuItem.selected').removeClass('selected');
	$this.addClass('selected');

	toggleHeaderEffect();
	socket.emit('callModule', $this.attr('module'), $this.attr('method'));
});

socket.on('setRealContent', function(html) {
	$('#effect').removeClass('coolAnimation');
	$('#realContent').html(html);
})