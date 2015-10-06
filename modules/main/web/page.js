$('.menuItem').click(function() {
	$this = $(this);
	$('.menuItem.selected').removeClass('selected');
	$this.addClass('selected');

	socket.emit('callModule', $this.attr('module'), $this.attr('method'));
})