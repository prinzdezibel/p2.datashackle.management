// Copyright (C) projekt-und-partner.com, 2011
// Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

namespace("p2.Span.Action");

p2.Span.Action = function(el, sourceId, info){
    var self = this;

    this.info = info;

    this.rootEl = el;
    this.sourceId = sourceId;
        
   
   	if (info.operational == false){
        this.registerDataNode();
    }
    
    var click = function(event){
        if (self.info.msg_reset){
            $(el).trigger('P2_RESET', []);
        }
        if (self.info.msg_close){
            $(el).trigger('P2_CLOSE', []);
        }
    }

    $(el).bind('click', click);
}

p2.Span.Action.prototype = function(){
    function instance(){};
	instance.prototype = p2.Span.prototype;
	var obj = new instance();
    return obj;
}();

p2.Span.Action.prototype.constructor = p2.Span;


