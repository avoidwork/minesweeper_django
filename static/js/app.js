( function ( document, window, $ ) {
	var $auth   = $( "#authArea" ),
	    $form   = $( "#authForm" ),
	    NOTHASH = /.*#/;

	$auth.hide();

	// Click listeners on auth buttons parentNode
	$( ".profileOptions" ).on( "click", function ( ev ) {
		var $ev     = $( ev ),
		    $target = $( ev.target );

		$ev.stop();
		$auth.hide();

		$.get( $target[0].href.replace( NOTHASH, "" ) + "/" ).then( function ( arg ) {
			$auth.html( arg );
			$auth.show();
		}, function ( e ) {
			$auth.html( "Something went wrong" );
			$auth.show();
		} );
	} );

	// Clearing hash on load
	document.location.hash = "";
} )( document, window, jQuery );
