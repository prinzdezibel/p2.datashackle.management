// Copyright (C) projekt-und-partner.com, 2010
// Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

namespace("p2.Span.Relation");

p2.Span.Relation = function(el, sourceId, info, targetResource, collectionId){
    var self = this;
    
    this.info = info;
    this.targetResource = targetResource;
    this.rootEl = el;
    this.sourceId = sourceId;
    this.collectionId = collectionId;
        
   	if (info.operational == false && !info.archetype){
        this.registerDataNode();
        
        // resizable button handler
	    $(el).find('.resizable').each(function(){
	        $(this).target = el;
	        $(this).css('top', '100%');
	        $(this).mousedown(function(ev){
	            self.resizableMousedown(ev);
	            return false;
	        });
	    });
    }

    this.initializeVisibility();
}

p2.Span.Relation.prototype = function(){
    function instance(){};
	instance.prototype = p2.Span.prototype;
	var obj = new instance();
    return obj;
}();

p2.Span.Relation.prototype.constructor = p2.Span;


p2.Span.Relation.prototype.onEditClick = function(){
    var setobjectId = this.info.data_node_id;
    var relationId = this.info.span_identifier;
    var isMultiSelectable = null; // Not relevant for now
    var picker = new p2.ObjectPicker(setobjectId, relationId, isMultiSelectable, this.collectionId);
    picker.open(this.targetResource);
    return false; // prevent default event handling
}
