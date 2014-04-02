( function ( document, window, $ ) {
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
	this.cookie  = cookie;
	this.element = target;
	this.game    = game;
	this.max_x   = max_x;
	this.max_y   = max_y;
	this.moves   = moves;
	this.token   = $.cookie( "csrftoken" );
}

/**
 * Click handler
 *
 * @method click
 * @param  {Object} ev MouseEvent
 * @return {Object}   Minesweeper instance
 */
Minesweeper.prototype.click = function ( ev ) {
	var $target = $( ev.target ),
	    $x      = $target.data( "x" ),
	    $y      = $target.data( "y" ),
	    success, error
	
	success = function ( arg ) {
		if ( arg.result === "success" ) {
			arg.clear.forEach( function ( i ) {
				this.move( {x: i.x, y: i.y} );
			}.bind( this ) );

			if ( arg.complete ) {
				this.completed( true );
			}
		}
		else {
			this.mine( {x: $x, y: $y} );
		}
	}

	error = function ( err ) {
		console.error( err );
	}

	ev.preventDefault();

	if ( $target.hasClass( "clickable" ) ) {
		$.ajax( {
			type    : "POST",
			url     : "move/",
			success : success.bind( this ),
			error   : error,
			data    : {game: this.game, x: $x, y: $y},
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
Minesweeper.prototype.completed = function ( arg ) {
	$( ".clickable" ).removeClass( "clickable" );
	$( this.element ).off( "click" );
	$( this.element.parentNode ).append( arg ? "<h3>This game was won!</h3>" : "<h3>This game was lost, sad face.</h3>" );

	return this;
};

/**
 * Handling clicking on a `mine`, the game is over!
 *
 * @method mine
 * @param  {Object} arg Object describing the position ({x: n, y:n})
 * @return {Object}     Minesweeper instance
 */
Minesweeper.prototype.mine = function ( arg ) {
	$( ".block[data-y='" + arg.y + "'][data-x='" + arg.x + "']" ).addClass( "mine glyphicon glyphicon-remove" );
	this.completed( false );

	return this;
};

/**
 * Makes a 'move'
 *
 * @method move
 * @param  {Object} arg Object describing the position ({x: n, y:n})
 * @return {Object}     Minesweeper instance
 */
Minesweeper.prototype.move = function ( arg ) {
	$( ".block[data-y='" + arg.y + "'][data-x='" + arg.x + "']" ).addClass( "clicked" ).removeClass( "clickable" );

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
			html.push( "<div class=\"block clickable\" data-y=\"" + i + "\" data-x=\"" + j + "\"></div>" );
		}
	}
	
	// Rendering the board
	$element.html( html.join( "\n" ) );

	// Playback previous moves
	this.playback();

	// Setting click handler
	$element.on( "click", this.click.bind( this ) );

	return this;
};

window.minesweeper = minesweeper;

} )( document, window, jQuery );