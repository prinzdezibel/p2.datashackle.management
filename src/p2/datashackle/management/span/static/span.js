// Copyright (C) projekt-und-partner.com, 2010
// Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

namespace("p2.Span");

p2.Span = function(el, sourceId, info){
    var self = this;

    this.info = info;
    
    this.rootEl = el;
   
    this.setStyle() 
    $(this.rootEl).attr('data-span-type', this.info.span_type);
    $(this.rootEl).attr('data-node-id', this.info.data_node_id);
    this.sourceId = sourceId;
        
    $(this.rootEl).find('textarea').bind('click', function(event){
        event.bubbles = false;
        $(this).focus();
        return false;
   });
   
   	// resizable button handler
   	if (info.operational == false && !info.archetype){
	    $(this.rootEl).find('.resizable').each(function(){
	        $(this).mousedown(function(ev){
	            self.resizableMousedown(ev);
	            return false;
	            }
	        );
	    });
	}

    this.initializeVisibility();
}

p2.Span.prototype.initializeVisibility = function(){
    var self = this;
    // Evaluate initial visible state.
    this.setVisibility(this.info.visible);
    var eventName = p2.datashackle.core.buildChangeEventName(this.info.type, this.info.span_identifier, 'visible');
    $(document).bind(eventName, function(e, senderEl, value){
        self.setVisibility(value);
    });
}

p2.Span.prototype.setVisibility = function(isVisible){
    if (isVisible){
		$(this.rootEl).show();
    }else{
		$(this.rootEl).hide();
    }
}

p2.Span.prototype.resizableMousedown = function(ev){
	var self = this;
	var originalX = ev.clientX;
	var originalY = ev.clientY;
	var originalWidth = $(ev.target).prev().width();
	var originalHeight = $(ev.target).prev().height();
    var mousemoveFn = function(){
	    var args = Array.prototype.slice.call(arguments, 0);
	    args = args.concat([originalX, originalY, originalWidth, originalHeight]);
	    self.resizableMousemove.apply(self, args);
	    };
	$(document).bind('mousemove', mousemoveFn);	
	$(document).bind('mouseup', function(){
	    $(document).unbind('mousemove', mousemoveFn);

        var next = self.rootEl;
        while(true){
            next = $(next).next('.p2-span');
            if (next.length == 0) break;
            // copy margin-left over to left position attribute.
            if ($(next).is(':visible')){
                var left = parseInt($(next).css('margin-left'));
                var pos = $(next).position();
                $(next).css('margin-left', 0);
                $(next).css('left', left + pos.left + 'px');
                var graphnode = p2.datashackle.core.session.graph.lookupGraphObject($(next).data('data-object').info.data_node_id);
                graphnode.vertex.setAttr('css', $(next).attr('style'));
            }
        }

	    // set new css value in setobject graph
        var setobject = p2.datashackle.core.session.lookupDataNode(self.info.data_node_id);
        setobject.setAttr('css', $(self.rootEl).attr('style'));
	});
};


p2.Span.prototype.resizableMousemove = function(ev, originalX, originalY, originalWidth, originalHeight){
    var deltaX = ev.clientX - originalX;
    var deltaY = ev.clientY - originalY;
    var width = originalWidth + deltaX;
    var height = originalHeight + deltaY;
    $(this.rootEl).width(width);
    $(this.rootEl).height(height);

    var next = this.rootEl;
    while(true){
        next = $(next).next('.p2-span');
        if (next.length == 0) break;
        // temporarily adjust left margin. When dragging is stopped, we add this
        // to the left position.
        $(next).css('margin-left', deltaX + 'px');
    }

    // Inform parent widget about the changes
    $(this.rootEl).trigger('MSG_SIZE_CHANGE', [width, height]);
    $(document).trigger('global-mark-dirty');
}

p2.Span.prototype.setStyle = function(){
    // Setting the style does potentially alter the span's dimension. Fire event.
    // $(this.rootEl).attr('style', this.info.css);
   
    
    var width = $(this.rootEl).width();
    var height = $(this.rootEl).height();
    $(this.rootEl).trigger('MSG_SIZE_CHANGE', [width, height]);
}

p2.Span.prototype.getDataID = function(el){
    var formEl = $(el).closest('.p2-form');
    var dataid = $(formEl).attr('data-node-id');
    return dataid;
}

p2.Span.prototype.registerDataNode = function(){
    var inputEl = $(this.rootEl).find('.input');
    if (this.info.span_type == 'Checkbox'){
        var initValue = $(inputEl).is(':checked') ? 1 : null; // Little hack to make the checkbox datatype work with
                                                              // String and Boolean database fields. In designer mode
                                                              // the checkbox state is saved as string in "span_value".
    }else{
        var initValue = $(inputEl).val();
    }
    var setobject = p2.datashackle.core.session.registerDataNode(this.info.type, this.info.data_node_id, this.info.action);
    if (this.sourceId != null){
        var linkageVertex = p2.datashackle.core.session.graph.lookupGraphObject(this.sourceId);
        if (!this.info.operational){
            // In designer mdoe, the span is hard-linked to its parent widget
            linkageVertex.vertex.link(this.info.data_node_id);
        }
    }
    var value = setobject.offerSetAttr(this.info.attr_name, initValue, this.info.span_identifier);
    var dataid = this.getDataID(inputEl);
    // Set it in case offersetAttr doesn't like the offered value.
    $(inputEl).val(value);
  

    p2.datashackle.core.handleChangeEvent(inputEl, setobject, this.info.span_type, this.info.attr_name, this.info.span_identifier);
    
    var fn_ignore = function(e, givendataid) {
        if (dataid == givendataid) {
            //change our action to ignore
            setobject.setAction.apply(setobject, ['ignore']);
        }
    }
    $(document).bind('form-setobjectaction-ignore', fn_ignore);
    
    var fn_save = function(e, givendataid) {
        if (dataid == givendataid) {
            setobject.setAction('save');
        }
    }
    $(document).bind('form-setobjectaction-save', fn_save);

    var fn_revert = function(e, givendataid) {
        if (dataid == givendataid) {
            $(document).unbind(e, fn_revert);
            $(document).unbind(e, fn_ignore);
            $(document).unbind(e, fn_save);
        }
    }
    $(document).bind('form-revert', fn_revert);


    if (!this.info.operational){
        // setobject.setAttr('css', this.info.css);
        setobject.setAttr('span_name', this.info.span_name);
    }
    
    this.setobject = setobject;
    return setobject;
}


