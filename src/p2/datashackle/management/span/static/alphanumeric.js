// Copyright (C) projekt-und-partner.com, 2010
// Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

namespace("p2.Span.Alphanumeric");

p2.Span.Alphanumeric = function(el, sourceId, applicationUrl, info){
    var self = this;
    this.info = info;
    this.rootEl = el;
    this.sourceId = sourceId;
    this.applicationUrl = applicationUrl;

    if (info.operational){
        var value = info.piggyback;
        $(el).find('textarea').html(info.piggyback);
    }else{
        var value = info.span_value;
        $(el).find('textarea').html(info.span_value);
    }
    
    // Set the text of the textarea
    if (info.operational){
        $(el).find('textarea').html(info.piggyback);
    }else{
        $(el).find('textarea').html(info.span_value);
    }

    this.createInputField(info.multi_line, value, false);

    if (info.archetype == false) {
        this.registerDataNode();
    }
  
    this.bindResizables(); 
    this.bindMultiline();
}

p2.Span.Alphanumeric.prototype = function(){
    function instance(){};
	instance.prototype = p2.Span.prototype;
	return new instance();
}();

p2.Span.Alphanumeric.prototype.constructor = p2.Span;


p2.Span.Alphanumeric.prototype.bindResizables = function(){
    var self = this;
   	// resizable button handler
   	if (this.info.operational == false){
	    $(this.rootEl).find('.resizable').each(function(){
	        $(this).mousedown(function(ev){
	            self.resizableMousedown(ev);
	            return false;
	            }
	        );
	    });
	}
}

p2.Span.Alphanumeric.prototype.setMultiline = function(multiline){
    var value = $(this.rootEl).find('.input').val();
    this.createInputField(multiline, value, true);
    if (multiline){
        this.info.multi_line = true;
    }else{
        this.info.multi_line = false;
    }
}

p2.Span.Alphanumeric.prototype.createInputField = function(multiline, value, setHeight){
    $(this.rootEl).empty();
    if (multiline){
        var textarea = $('<textarea class="input" />');
        textarea.html(value);
        $(this.rootEl).append(textarea);
        if (setHeight) $(this.rootEl).height(45);
        textarea.bind('click', function(event){
           event.bubbles = false;
           $(this).focus();
           return false;
        });
    }else{
        var textline = $('<input type="text" class="input" />');
        textline.val(value);
        $(this.rootEl).append(textline);
        if (setHeight) $(this.rootEl).height(17);
    }
    
    if (!this.info.operational){
        var resizer = $('<div class="resizable" alt="Resize handle" />');
        resizer.css('background-image', 'url(' + this.applicationUrl + '/@@/setmanager.ui.skin/control_resizable.gif)');
        $(this.rootEl).append(resizer);
    }
    if (setHeight){
        var setobject = p2.datashackle.core.session.lookupDataNode(this.info.data_node_id);
        this.setStyle();
    }
    
    this.bindResizables();
}


p2.Span.Alphanumeric.prototype.resizableMousemove = function(ev, originalX, originalY, originalWidth, originalHeight){
    var deltaX = ev.clientX - originalX;
    var deltaY = ev.clientY - originalY;
    var width = originalWidth + deltaX;
    var height = originalHeight + deltaY;
    if (this.info.multi_line){
        if (height < 45){
            height = 45;
        }
        $(this.rootEl).height(height);
    }
    $(this.rootEl).width(width);

    // Inform parent widget about the changes
    $(this.rootEl).trigger('MSG_SIZE_CHANGE', [width, height]);
    $(document).trigger('global-mark-dirty');
}

p2.Span.Alphanumeric.prototype.getDataID = function(el){
    var formEl = $(el).closest('.p2-form');
    var dataid = $(formEl).attr('data-node-id');
    return dataid;
}

p2.Span.Alphanumeric.prototype.bindMultiline = function(){
    var self = this;
    var eventName = p2.datashackle.core.buildChangeEventName(this.info.module, this.info.type, this.info.span_identifier, 'multi_line');
    $(document).bind(eventName, function(e, senderEl, value){
        self.setMultiline(value); 
    });
}

p2.Span.Alphanumeric.prototype.registerDataNode = function(){
    var inputEl = $(this.rootEl).find('.input');
    var initValue = $(inputEl).val();
    var setobject = p2.datashackle.core.session.registerDataNode(this.info.module, this.info.type, this.info.data_node_id, this.info.action);
    if (this.sourceId != null){
        var linkageVertex = p2.datashackle.core.session.graph.lookupGraphObject(this.sourceId);
        
        if (!this.info.operational){
            // In designer mdoe, the span is hard-linked to its parent widget
            linkageVertex.vertex.link(this.info.data_node_id);
        }
    }
    var span_identifier = this.info.operational ? this.info.span_identifier : null;
    var value = setobject.offerSetAttr(this.info.attr_name, initValue, span_identifier);
    var dataid = this.getDataID(inputEl);
    //set in case the offerSetAttr does not like the offered value
    $(inputEl).val(value);

    p2.datashackle.core.handleChangeEvent(inputEl, setobject, this.info.span_type, this.info.attr_name, span_identifier);
   
    // various custom event bindings - those allow controlling this setobject easily without having a js reference to it
    
    var fn_ignore = function(e, givendataid) {
        if (dataid == givendataid) {
            //change our action to ignore
            setobject.setAction('ignore');
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
         this.setStyle();
         setobject.setAttr('span_name', this.info.span_name);
    }   
 
    return setobject;
}


