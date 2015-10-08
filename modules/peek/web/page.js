if(typeof window.logMessageHooked === "undefined") {
	window.logMessageHooked = true;
	socket.on('logMessage', function(logm) {
		$('#peekChat').html($('#peekChat').html() + logm);

		if($('chatItem').length > 10) {
			$('chatItem:first').remove();
		}
	});
}