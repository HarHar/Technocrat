if(typeof window.logMessageHooked === "undefined") {
	socket.on('logMessage', function(logm) {
		window.logMessageHooked = true;
		$('#peekChat').html($('#peekChat').html() + logm);

		if($('chatItem').length > 10) {
			$('chatItem:first').remove();
		}
	});
}