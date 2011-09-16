// Copyright (C) projekt-und-partner.com, 2011
// Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

namespace("p2.Span.Dropdown");

p2.Span.Dropdown = function(el, sourceId, info, targetResource, collectionId){
    var self = this;
    
    this.info = info;
    this.targetResource = targetResource;
    this.rootEl = el;
    this.sourceId = sourceId;
    this.collectionId = collectionId;
        
   	if (info.operational == false && !info.archetype){
        this.registerDataNode();
        
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
   
    var $sel = $(this.rootEl).find('select');
    if ($sel.length != 1) throw Error("No or more than one select element found.");
    $sel.bind('change', function(){
	    var args = Array.prototype.slice.call(arguments, 1);
        self.onChange.apply(self, [this].concat(args));
    });
}

p2.Span.Dropdown.prototype = function(){
    function instance(){};
	instance.prototype = p2.Span.prototype;
	var obj = new instance();
    return obj;
}();

p2.Span.Dropdown.prototype.constructor = p2.Span;

p2.Span.Dropdown.prototype.onChange = function(sel, ev){
    //set the new vertex link
	var linkageVertex = p2.datashackle.core.session.graph.lookupGraphObject(this.collectionId);
    var val = $(sel).val();
    if (val == ""){
        // an empty dropdown entry
        val = null;
    }
    linkageVertex.vertex.link(val);
    //mark setobject as changed
    p2.datashackle.core.triggerChangeOnElement(sel);
}
