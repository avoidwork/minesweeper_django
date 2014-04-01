( function ( $ ) {
	var $resume = $( ".resume" ),
	    $game   = $.cookie( "game" );

	if ( $game ) {
		$resume.attr( "href", "/games/" + $game + "/" )
		       .removeClass( "hidden" );
	}
} )( jQuery );
