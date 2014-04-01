( function ( document, window, $ ) {
	var $auth   = $( "#authArea" ),
	    $form   = $( "#authForm" ),
	    $csrf   = $.cookie( "csrftoken" ),
	    NOTHASH = /.*#/;

	$auth.hide();

	// Prepares a form submission
	function submit ( type, success, error ) {
		var data = {};

		// Clearing error message
		$( ".error" ).html( "" );

		// Gathing form data
		$form.find( "input" ).each( function ( idx, i ) {
			data[i.id] = i.value;
		} );

		// Comparing if applicable
		if ( data.password_2 !== undefined && data.password !== data.password_2 ) {
			return $( ".error" ).html( "Passwords do not match" );
		}

		return $.ajax( {
			type    : "POST",
			url     : type + "/",
			data    : data,
			success : success,
			error   : error,
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
		    $type   = $target[0].href.replace( NOTHASH, "" ),
		    success, error;

		success = function ( arg ) {
			$auth.html( arg );
			$auth.show();

			$auth.find( "a[href='#submit']" ).on( "click", function ( ev ) {
				ev.preventDefault();
				$( ev ).stop();

				submit( $type, ready, function ( e ) {
					$( ".error" ).html( "Something went wrong" );
				} );
			} );

			$auth.find( "a[href='#reset']" ).on( "click", function ( ev ) {
				ev.preventDefault();
				$( ev ).stop();
				$form[0].reset();
			} );
		};

		error = function ( e ) {
			$auth.html( "Something went wrong" );
			$auth.show();
		};

		$ev.stop();
		$auth.hide();

		$.ajax( {
			type    : "GET",
			url     : $type + "/",
			success : success,
			error   : error
		} );
	} );

	// Clearing hash on load
	document.location.hash = "";
} )( document, window, jQuery );
