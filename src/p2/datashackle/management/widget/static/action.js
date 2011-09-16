// Copyright (C) projekt-und-partner.com, 2011
// Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

namespace("p2");

p2.ActionWidget = function(element, operational, propertyform, options){
    p2.Widget.call(this, element, operational, propertyform);
    
    this.options = options;
    
    var self = this; 
    var click = function(event){
        if (self.options.msg_reset){
            $(element).trigger('P2_RESET', []);
        }
        if (self.options.msg_close){
            $(element).trigger('P2_CLOSE', []);
        }
    }

    $(element).bind('click', click);    
}

p2.ActionWidget.prototype = function(){
    function instance(){};
	instance.prototype = p2.Widget.prototype;
	return new instance();
}();

p2.ActionWidget.prototype.constructor = p2.Widget;


