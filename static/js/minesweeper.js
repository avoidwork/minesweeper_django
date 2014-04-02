function minesweeper ( target, moves ) {
	return new Minesweeper( target, moves || [] );
}

function Minesweeper( target, moves ) {
	this.element = target;
	this.moves   = moves;
	this.wired   = true;
}

/**
 * Makes a 'move', sends to the server if `wired`
 *
 * @method move
 * @param  {Object} arg Object describing the move ({x: n, y:n, epoch:n})
 * @return {Object}     Minesweeper instance
 */
Minesweeper.prototype.move = function ( arg ) {

};

Minesweeper.prototype.playback = function () {
	this.wired = false;

	this.moves.forEach( function ( i ) {
		this.move( i );
	}, this );

	this.wired = true;

	return this;
};
