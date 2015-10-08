var spinner = '<div class="spinner"> <div class="rect1"></div> <div class="rect2"></div> <div class="rect3"></div> <div class="rect4"></div> <div class="rect5"></div> </div>'
if(typeof window.reportHooked === "undefined") {
	window.reportHooked = true;

	$('#reportSubmit').click(function() {
		$(spinner).insertAfter('#reportSubmit');
		$('#reportSubmit').remove();
		$('input').attr('disabled', 'disabled');
		socket.emit('callModule', 'report', 'submitReport', $('#userName').val(), $('#reason').val());
	});
}