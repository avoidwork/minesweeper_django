( function ( document, window, $ ) {
	var $auth   = $( "#authArea" ),
	    $form   = $( "#authForm" ),
	    $csrf   = $.cookie( "csrftoken" ),
	    NOTHASH = /.*#/;

	$auth.hide();

	// Prepares a form submission
	function submit ( type ) {
		var data = {};

		$form.find( "input" ).each( function ( idx, i ) {
			data[i.id] = i.value;
		} );

		return $.ajax( {
			type    : "POST",
			url     : type + "/",
			data    : data,
			headers : {"X-CSRFToken": $csrf}
		} );
	}

	// Ready to start/resume a game
	function ready ( arg ) {
		debugger;
	}

	// Click listeners on auth buttons parentNode
	$( ".profileOptions" ).on( "click", function ( ev ) {
		var $ev     = $( ev ),
		    $target = $( ev.target ),
		    $type   = $target[0].href.replace( NOTHASH, "" );

		$ev.stop();
		$auth.hide();

		$.get( $type + "/" ).then( function ( arg ) {
			$auth.html( arg );
			$auth.show();

			$auth.find( "a[href='#submit']" ).on( "click", function ( ev ) {
				ev.preventDefault();
				$( ev ).stop();

				submit( $type ).then( ready, function ( e ) {
					$( ".error" ).html( "Something went wrong" );
				} );
			} );

			$auth.find( "a[href='#reset']" ).on( "click", function ( ev ) {
				ev.preventDefault();
				$( ev ).stop();
				$form[0].reset();
			} );
		}, function ( e ) {
			$auth.html( "Something went wrong" );
			$auth.show();
		} );
	} );

	// Clearing hash on load
	document.location.hash = "";
} )( document, window, jQuery );
