$('#appealSubmit').click(function() {
	$('#appealSubmit').remove();
	$('textarea').attr('disabled', 'disabled');
	$('input').attr('disabled', 'disabled');
	socket.emit('callModule', 'banAppeal', 'submitAppeal', $('#appealArea').val());
});