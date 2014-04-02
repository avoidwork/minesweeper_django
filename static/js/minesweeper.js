( function ( document, window, $ ) {
/**
 * Logs errors to the console
 *
 * @method error
 * @param  {Object} err Error instance
 * @return {Undefined}  undefined
 */
function error ( err ) {
	console.error( err.stack || err.message || err );
}

/**
 * Minesweeper factory
 *
 * @method minesweeper
 * @param {Object} target Element
 * @param {String} game   Game ID
 * @param {Number} max_x  Maximum columns
 * @param {Number} max_y  Maximum rows
 * @param {String} cookie Cookie name
 * @param {Array}  moves  Previous moves
 * @return {Object}       Minesweeper instance
 */
function minesweeper ( target, game, max_x, max_y, cookie, moves ) {
	return new Minesweeper( target, game, max_x, max_y, cookie, moves );
}

/**
 * @constructor
 * @param {Object} target Element
 * @param {String} game   Game ID
 * @param {Number} max_x  Maximum columns
 * @param {Number} max_y  Maximum rows
 * @param {String} cookie Cookie name
 * @param {Array}  moves  Previous moves
 */
function Minesweeper( target, game, max_x, max_y, cookie, moves ) {
	this.completed = false;
	this.cookie    = cookie;
	this.element   = target;
	this.flags     = 0;
	this.game      = game;
	this.max_x     = max_x;
	this.max_y     = max_y;
	this.moves     = moves;
	this.token     = $.cookie( "csrftoken" );
}

/**
 * Click handler
 *
 * @method click
 * @param  {Object} ev MouseEvent
 * @return {Object}    Minesweeper instance
 */
Minesweeper.prototype.click = function ( ev ) {
	var $target = $( ev.target ),
	    $x, $y, success;

	// Flag
	if ( ev.target.nodeName === "I" ) {
		$target = $( ev.target.parentNode );
	}

	$x = $target.data( "x" );
	$y = $target.data( "y" );
	
	success = function ( arg ) {
		if ( arg.result === "success" ) {
			$target.addClass( "clicked" );
			arg.moves.forEach( this.move );

			if ( arg.complete ) {
				this.complete( true );
			}
		}
		else {
			this.mine( {x: $x, y: $y} );
		}
	}

	ev.preventDefault();

	if ( $target.hasClass( "clickable" ) ) {
		$.ajax( {
			type    : "POST",
			url     : "move/",
			success : success.bind( this ),
			error   : error,
			data    : {game: this.game, x: $x, y: $y, flag: false},
			headers : {"X-CSRFToken": this.token}
		} );
	}

	return this;
};

/**
 * Marks the game as 'complete'
 *
 * @method completed
 * @param  {Boolean} arg `true` if game was won
 * @return {Object}      Minesweeper instance
 */
Minesweeper.prototype.complete = function ( arg ) {
	var $parent = $( this.element.parentNode );

	this.completed = true;

	$( ".clickable" ).removeClass( "clickable" );
	$( this.element ).off( "click" );
	$.removeCookie( "game", {path: "/"} );

	$parent.append( arg ? "<h3><i class=\"fa fa-smile-o\"></i> This game was won!</h3>" : "<h3><i class=\"fa fa-frown-o\"></i> This game was lost, sad face.</h3>" );
	$parent.append( "<p class=\"pad-top options new\"><a class=\"btn btn-lg btn-success\" href=\"/games/new/\" role=\"button\"><i class=\"fa fa-rocket\"></i> New Game</a></p>" );

	return this;
};

/**
 * Handling clicking on a `mine`, the game is over!
 *
 * @method mine
 * @param  {Object} arg Object describing the position
 * @return {Object}     Minesweeper instance
 */
Minesweeper.prototype.mine = function ( arg ) {
	$( ".block[data-y='" + arg.y + "'][data-x='" + arg.x + "']" ).addClass( "mine" ).html( " <i class=\"fa fa-cog\"></i>" );
	this.complete( false );

	return this;
};

/**
 * Makes a 'move'
 *
 * @method move
 * @param  {Object} arg Object describing the position
 * @return {Object}     Minesweeper instance
 */
Minesweeper.prototype.move = function ( arg ) {
	var $element = $( ".block[data-y='" + arg.y + "'][data-x='" + arg.x + "']" );

	switch ( true ) {
		case arg.flag:
			$element.html( "<i class=\"fa fa-flag\"></i>" );
			this.flags++;
			$( "#flags" ).html( this.flags );
			break;
		case arg.click:
		case arg.mines === 0:
			if ( $element[0].childNodes.length > 0 ) {
				this.flags--;
				$( "#flags" ).html( this.flags );
			}

			$element.html( "" ).addClass( "clicked" ).removeClass( "clickable" );
			break;
		default:
			$element.html( arg.mines );
	}

	$element.data( "mines", arg.mines );

	return this;
};

/**
 * Plays back a series of moves
 *
 * @method playback
 * @return {Object} Minesweeper instance
 */
Minesweeper.prototype.playback = function () {
	this.moves.forEach( function ( i ) {
		this.move( i );
	}, this );

	return this;
};

/**
 * Renders the board
 *
 * @method render
 * @return {Object} Minesweeper instance
 */
Minesweeper.prototype.render = function () {
	var html     = [],
	    $element = $( this.element ),
	    nth1     = this.max_y,
	    nth2     = this.max_x,
	    i, j;

	// Generating the peices
	i = -1;
	while ( ++i < nth1 ) {
		j = -1;
		while ( ++j < nth2 ) {
			html.push( "<div class=\"block clickable\" data-y=\"" + i + "\" data-x=\"" + j + "\" data-mines=\"0\"></div>" );
		}
	}
	
	// Rendering the board
	$element.html( html.join( "\n" ) );

	// Playback previous moves
	this.playback();

	// Setting click handlers
	$element.on( "click", this.click.bind( this ) );
	$element.on( "contextmenu", this.rightClick.bind( this ) );

	return this;
};

/**
 * Click listener for the context menu
 *
 * @method rightClick
 * @param  {Object} ev Mouse Event
 * @return {Object}    Minesweeper instance
 */
Minesweeper.prototype.rightClick = function ( ev ) {
	var target  = ev.target,
	    flagged = true,
	    $target, $x, $y;

	ev.preventDefault();

	if ( !this.completed ) {
		if ( target.nodeName === "I" ) {
			target = target.parentNode;
		}

		$target = $( target );
		$x      = $target.data( "x" );
	    $y      = $target.data( "y" );

		if ( target.childNodes.length > 0 && $( target.childNodes[0] ).hasClass( "fa-flag") ) {
			$.ajax( {
				type    : "POST",
				url     : "move/",
				success : function ( arg ) {
					if ( arg.result === "success" ) {
						$( target.childNodes[0] ).remove();

						if ( parseInt( $target.data( "mines" ), 10 ) > 0 ) {
							$target.html( $target.data( "mines" ) );
						}

						this.flags--;
						$( "#flags" ).html( this.flags );
					}
					else {
						this.mine( {x: $x, y: $y} );
					}
				}.bind( this ),
				error   : error,
				data    : {game: this.game, x: $x, y: $y, flag: flagged},
				headers : {"X-CSRFToken": this.token}
			} );
		}
		else if ( this.flags < 10 ) {
			$.ajax( {
				type    : "POST",
				url     : "move/",
				success : function () {
					$target.html( "<i class=\"fa fa-flag\"></i>" );
					this.flags++;
					$( "#flags" ).html( this.flags );
				}.bind( this ),
				error   : error,
				data    : {game: this.game, x: $x, y: $y, flag: flagged},
				headers : {"X-CSRFToken": this.token}
			} );
		}
	}

	return this;
};

window.minesweeper = minesweeper;

} )( document, window, jQuery );