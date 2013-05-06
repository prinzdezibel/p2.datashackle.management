// Arrange windows in a given sreen estate so they don't overlap.

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// A copy of the GNU General Public License is included in the
// documentation.

// Copyright (C): projekt-und-partner.com, 2010
//
// Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

namespace("p2")


p2.BinPacker = function(containerWidth, padding){
	p2.BinPacker.containerWidth = containerWidth;
	this.pieces = new Array();
	if (!padding){
		p2.BinPacker.padding = {
			top: 0,
			right: 0,
			bottom: 0,
			left: 0
			};
	}else{
		p2.BinPacker.padding = padding;
	}
}

p2.BinPacker.prototype.addPiece = function(piece){
	this.pieces.push(piece);
}

p2.BinPacker.prototype.generatePackingPlan = function(){
	// As pieces get "consumed" during packing process,
	// we need to make a copy from it
	this.freePieces = this.pieces.slice(0);
	
	var layerOffset = 0;
	var packingPlan = Array();
	//for(index in this.freePieces)
	while (this.freePieces.length != 0){
		// We take the piece with the greates height as
		// layer defining piece (ldp).
		var maxHeight = 0;
		var maxHeightIndex = null;
		for (var a = 0;	a < this.freePieces.length;	++a){
			if (this.freePieces[a].height > maxHeight){
				maxHeight = this.freePieces[a].height;
				maxHeightIndex = a;
			}
		}
		var ldp = this.freePieces[maxHeightIndex];
		p2.BinPacker.maxLayerThickness = ldp.height;
		var sBest = this._fillLayerNg(
				ldp,
				this.freePieces);

		for (var a in sBest.placements){
			var placement = sBest.placements[a];
			placement.placingPoint.y += layerOffset;
		}
		packingPlan = packingPlan.concat(sBest);
			
		// The algorithm has given the best to find
		// a good (hopefully the best :) packing scheme for this layer.
		// Now we remove the placed pieces from freePieces.
		for (index in sBest.placements){
			var placement = sBest.placements[index];
			// find placement in this.freePieces and remove it
			for(var i = 0; i < this.freePieces.length; ++i){
				var piece = this.freePieces[i];
				if (piece.id == placement.piece.id){
					this.freePieces.splice(i, 1);
				}
			}
		}
		layerOffset += p2.BinPacker.maxLayerThickness;
	}
	return packingPlan;
}

// The heuristic for filling a layer stems from the
// algorithm "Touching perimeter" from Lodi et al. (1999)
p2.BinPacker.prototype._fillLayerNg = function (ldp, freePieces) {
	// search depth
	var sDepth = 1;
	// search width
	var sWidth = 2;
	// set with search states. The best one is the resulting
	// search state (sBest).
	this.sSet = new Array();
	var sBest = null;
	var origin = new p2.BinPacker.PlacingPoint(
			0, 0,
			p2.BinPacker.containerWidth, 
			p2.BinPacker.maxLayerThickness);
	var placements = Array();	
	var placingPoints = new Array(origin);
	var firstState = new p2.BinPacker.SearchState(
			freePieces, placingPoints, placements);
	this.sSet[0] = firstState;
		
	while (this.sSet.length != 0){
		// select state s ∈ sSet with maximum number of packed pieces and
		// set sSet := sSet \ {s}  (remove it from sSet)
		var indexMax = this.selectMaxNpState();
		// Remove it from searchstate set.
		var maxNpState = this.sSet.splice(indexMax, 1)[0];
				
		if (maxNpState == firstState){
			// generate successor state S1 for
			// placement(r0, p0)
			var placement = new p2.BinPacker.Placement(ldp, origin);
			var state = maxNpState.genNextSearchState(placement);
			this.sSet.push(state);
		}else{
			// search state does not contain a complete solution, e.g.
			// it is still extensible
			if (maxNpState.packedPieces() <= sDepth){
				var nsucc = sWidth;
			}else{
				var nsucc = 1;
			}
			var placements = this._determinePermittedPlacements(
					maxNpState,
					nsucc
					);
			if (placements){
				//alert(placements.toSource());
				for (var i = 0; i < placements.length; i++){
					var placement = placements[i];
					var state = maxNpState.genNextSearchState(placement);
					this.sSet.push(state);
				}	
			}else{
				// state contains complete packing plan for layer
				// If it is better than the best existing one, update it.
				if (!sBest || maxNpState.packedValue > sBest.packedValue){
					sBest = maxNpState;
				}
			}
		}
	}
	return sBest;
}


// removes the searchstate s ∈ sSet where
// number of packed pieces is maximal
p2.BinPacker.prototype.selectMaxNpState = function(){
	var maxNp = 0;
	var indexMax = undefined;
	for(var i = 0; i < this.sSet.length; i++){
		if (this.sSet[i].packedPieces() >= maxNp){
			maxNp = this.sSet[i].packedPieces();
			indexMax = i;
		}
	}
	return indexMax;
}

// Determine (maximal) nsucc permitted placements (r, o, p)i with
// i = 1,...,nsucc 
// with highest tp values
p2.BinPacker.prototype._determinePermittedPlacements = function(state, max){
	var pp = new Array();
	for (var i = 0; i< state.freePieces.length; i++){
		var piece = state.freePieces[i];
		var tresholdTp = 0;
		// check available placing points
		for (var a = 0; a < state.placingPoints.length; a++){
			var placingPoint = state.placingPoints[a];
			// Does the piece's width fit there? The piece's front
			// edge may not exceed the rear edge of its upper neighbour.
			// (or the container top edge)
			if (placingPoint.y == 0){
				var deltaX = p2.BinPacker.containerWidth - placingPoint.x;
			}else{
				var deltaX = placingPoint.maxWidth;
			}
			if (piece.width > deltaX) continue; // not feasible
			
			//check height
			if (placingPoint.x == 0){
				var deltaY = p2.BinPacker.maxLayerThickness - placingPoint.y;
			}else{
				var deltaY = placingPoint.maxHeight;
			}
			if (piece.height > deltaY) continue; // not feasible
			
			// calculate the touching perimeter
			// (the contact edge on top).
			var tp = piece.width;
			// the leg on the left:
			tp += piece.height;
			// if the piece has contact to the container bottom, this
			// is also considered as touching perimeter length.
			if (piece.height == 
					(p2.BinPacker.maxLayerThickness - placingPoint.y)){
				tp += piece.width;
			}
			
			if (tp > tresholdTp){
				// append to end
				pp.push(new p2.BinPacker.Placement(
						piece,
						placingPoint,
						tp));
				if (pp.length >= max){
					break;
				}
				tresholdTp = tp;
			}
		}
	}
	
	if (pp.length > 0){
		return pp.slice(-max);	
	}else{
		return null;
	}
}


/**********************************************
 * Search state								  *
 **********************************************/
//A search state is given through a 3-tupel S = (R, P, Pl)
//with the following components:
//set of still free pieces R, set of placing points P
//and set of placements carried out Pl. 
p2.BinPacker.SearchState = function(freePieces,	placingPoints, placements){
	// the member variables are going to change! Don't pass in 
	// variables that are intended to be immutable.
	this.freePieces = freePieces;
	this.placingPoints = placingPoints;
	this.placements = placements;
}

p2.BinPacker.SearchState.prototype.packedPieces = function(){
	return this.placements.length;
}

p2.BinPacker.SearchState.prototype.packedValue = function(){
	var vp = 0; // packed value
	for (placement in this.placements){
		vp += placement.tp;
	}
	return vp;
}

// If a placement (r,o,p) is carried out in a search state S,
// the result is a successor state S’ (copy!), which is obtained through an
// updating of the components of S. In particular, placing point p 
// from S.Pl is to be replaced by new placing points situated on
// the rear and right edge of the placed piece (or on the extensions of
// these edges)
p2.BinPacker.SearchState.prototype.genNextSearchState = function(placement){
	// Because we are going delete the pieces for the
	// algorithm to work, we use a copy, not the original one.
	var freePieces = new Array();
	var placements = this.placements.slice(0);
	var placingPoints = this.placingPoints.slice(0);
	
	for (var i = 0; i < this.freePieces.length; i++){
		if (this.freePieces[i].id == placement.piece.id){
			// add it to placements
			placements.push(placement);
		}else{
			freePieces.push(this.freePieces[i]);
		}
	}
	
	// remove the placing point which is now occupied from placement
	for (var i = 0; i < placingPoints.length; i++){
		var placingPoint = placingPoints[i];
		
		if (placingPoint.x == placement.placingPoint.x &&
			placingPoint.y == placement.placingPoint.y){
			placingPoints.splice(i, 1);
		}
	}
	
	// upper right corner
	var pointX1 = placement.placingPoint.x + placement.piece.width;
	var pointY1 = placement.placingPoint.y;
	placingPoints.push(new p2.BinPacker.PlacingPoint(
			pointX1, pointY1,
			p2.BinPacker.containerWidth - pointX1,
			p2.BinPacker.maxLayerThickness - pointY1));

	// lower left corner
	var pointX2 = placement.placingPoint.x;
	var pointY2 = placement.placingPoint.y + placement.piece.height;
	placingPoints.push(new p2.BinPacker.PlacingPoint(
			pointX2, pointY2,
			p2.BinPacker.containerWidth - pointX2,
			p2.BinPacker.maxLayerThickness - pointY2));
	
	return new p2.BinPacker.SearchState(
			freePieces, placingPoints, placements);
}



/**********************************************
 * Pieces to be packed.                       *
 **********************************************/
p2.BinPacker.Piece = function(id, width, height) {
	this.id = id;
	this.width = parseInt(width) + p2.BinPacker.padding.left +
		p2.BinPacker.padding.right;
	this.height = parseInt(height) + p2.BinPacker.padding.top +
		p2.BinPacker.padding.bottom;
}

p2.BinPacker.PlacingPoint = function(x, y, maxWidth, maxHeight){
	this.x = x;
	this.y = y;
	this.maxWidth = maxWidth;
	this.maxHeight = maxHeight;
}

p2.BinPacker.Placement = function(piece, placingPoint, tp){
	this.piece = piece;
	this.placingPoint = placingPoint;
	// touching perimeter value
	this.tp = tp;
}

p2.BinPacker.Placement.prototype = {
	get x(){
		return this.placingPoint.x + p2.BinPacker.padding.left;
	},
	get y(){
		return this.placingPoint.y + p2.BinPacker.padding.top;
	}
}

