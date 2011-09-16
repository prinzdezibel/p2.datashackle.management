// Copyright (C) projekt-und-partner.com, 2011
// Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

namespace("p2.Span");

p2.Span.Checkbox = function(el, sourceId, info){
    p2.Span.call(this, el, sourceId, info);
    
    if (this.info.operational){
        $(el).find('input[type="checkbox"]').attr('checked', this.info.piggyback == 1 ? 'checked' : '');
    }
    if (info.archetype == false) {
        this.registerDataNode();
    }
}


p2.Span.Checkbox.prototype = function(){
    function instance(){};
	instance.prototype = p2.Span.prototype;
	return new instance();
}();

p2.Span.Checkbox.prototype.constructor = p2.Span;


