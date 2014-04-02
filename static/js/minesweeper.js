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
	this.online  = true;
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
 * Makes a 'move', sends to the server if `wired`
 *
 * @method move
 * @param  {Object} arg Object describing the move ({x: n, y:n, epoch:n})
 * @return {Object}     Minesweeper instance
 */
Minesweeper.prototype.mine = function ( arg ) {
	var $element = $( this.element ),
	    $parent = $( this.element.parentNode );

	$( ".block[data-y='" + arg.y + "'][data-x='" + arg.x + "']" ).addClass( "mine glyphicon glyphicon-remove" );
	$( ".clickable" ).removeClass( "clickable" );
	$element.off( "click" );
	$parent.append( "<h3>This game was lost, sad face.</h3>" );

	return this;
};

/**
 * Makes a 'move', sends to the server if `wired`
 *
 * @method move
 * @param  {Object} arg Object describing the move ({x: n, y:n, epoch:n})
 * @return {Object}     Minesweeper instance
 */
Minesweeper.prototype.move = function ( arg ) {
	$( ".block[data-y='" + arg.y + "'][data-x='" + arg.x + "']" ).addClass( "clicked" ).removeClass( "clickable" );

	return this;
};

/**
 * Plays back a series of moves
 * @return {Object} Minesweeper instance
 */
Minesweeper.prototype.playback = function () {
	this.online = false;

	this.moves.forEach( function ( i ) {
		this.move( i );
	}, this );

	this.online = true;

	return this;
};

/**
 * Renders the board
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

	// @todo clear pieces based on history

	// Setting click handler
	$element.on( "click", this.click.bind( this ) );

	return this;
};

window.minesweeper = minesweeper;

} )( document, window, jQuery );