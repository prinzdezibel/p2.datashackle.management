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
    
    if (!info.archetype && info.operational == false){
         // Span is not registered in operational mode.
         // We don't want it as prop element in graph.
         // Instead the linkage is registered.
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
    
    if(info.operational == true){
        // handleChangeEvent is normally called in registerDataNode
        var inputEl = $(this.rootEl).find('.input');
        var eventName = p2.datashackle.core.buildChangeEventName(this.info.module, this.info.type, this.info.data_node_id, this.info.attr_name);
        // change event binding
        $(inputEl).bind('change', function(e){
            var value = $(inputEl).val();
            p2.datashackle.core.triggerChangeOnElement(inputEl);
            $(document).trigger(eventName, [inputEl, value]);
            return true;
        });

        // Register on document scopt onto this event, so that dropdown
        // is getting updated, whenever the same dropdown is displayed and
        // changed somewhere else. 
        $(document).bind(eventName, function(e, senderEl, value){
            if (inputEl != senderEl){
                $(inputEl).val(value);
            }
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
