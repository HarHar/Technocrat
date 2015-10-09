if(typeof window.accessHooked === "undefined") {
	window.accessHooked = true;
}

$('#loginSubmit').click(function() {
	socket.emit('callModule', 'access', 'doLogin', $('#login_nick').val());
	$('input').attr('disabled', 'disabled');
	$('#loginSubmit').val('Logging in...');
});