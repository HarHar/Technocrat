$('#feedbackSubmit').click(function() {
	$(spinner).insertAfter('#reportSubmit');
	$('#feedbackSubmit').remove();
	$('textarea').attr('disabled', 'disabled');
	$('input').attr('disabled', 'disabled');
	socket.emit('callModule', 'feedback', 'submitFeedback', $('textarea').val());
});

$('#goLogin').click(function() {
	$('.menuItem.selected').removeClass('selected');
	$('#access.menuItem').addClass('selected');

	socket.emit('callModule', 'access', 'showAccess');
	window.toggleHeaderEffect();
})
