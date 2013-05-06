// Copyright (C) projekt-und-partner.com, 2010
// Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

namespace("p2.Span.Label");

p2.Span.Label = function(el, sourceId, info){
    p2.Span.call(this, el, sourceId, info);
    
    // Set the text of the textarea
    if (!info.operational){
        $(el).find('textarea').html(info.span_value);
        if (!info.archetype) {
            this.registerDataNode();
        }
    }
}

p2.Span.Label.prototype = function(){
    function instance(){};
	instance.prototype = p2.Span.prototype;
	var obj = new instance();
    return obj;
}();

p2.Span.Label.prototype.constructor = p2.Span;

