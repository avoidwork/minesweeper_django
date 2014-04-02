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
	    $y      = $target.data( "y" );

	ev.preventDefault();

	debugger;

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
	var $block = $( "data[x='" + arg.x + "', y='" + arg.y + "']");

	if ( this.online ) {

	}
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

	// Setting click handler
	$element.on( "click", this.click );

	return this;
};

window.minesweeper = minesweeper;

} )( document, window, jQuery );