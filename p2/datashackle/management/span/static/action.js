// Copyright (C) projekt-und-partner.com, 2011
// Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

namespace("p2.Span.Action");

p2.Span.Action = function(el, sourceId, info, actionurl){
    var self = this;

    this.info = info;
    this.actionurl = actionurl;
    this.rootEl = el;
    this.sourceId = sourceId;
       
   
   	if (info.operational == false){
        this.registerDataNode();
    }
}

p2.Span.Action.prototype = function(){
    function instance(){};
	instance.prototype = p2.Span.prototype;
	var obj = new instance();
    return obj;
}();

p2.Span.Action.prototype.constructor = p2.Span;


