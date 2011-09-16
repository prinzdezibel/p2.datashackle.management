// Copyright (C) projekt-und-partner.com, 2011
// Author:  Jonas Thiem <jonas.thiem%40projekt-und-partner.com>

namespace("p2.Widget.Fileupload");

p2.Widget.Fileupload = function(element, operational, propertyform) {
    p2.Widget.call(this, element, operational, propertyform);
}

p2.Widget.Fileupload.prototype = function(){
    function instance(){};
	instance.prototype = p2.Widget.prototype;
	return new instance();
}();

p2.Widget.Fileupload.prototype.constructor = p2.Widget;


p2.Widget.Fileupload.prototype.calcWidth = function() {
    var width = 0;
    $(this.rootEl).children('.p2-span').each(function(){
        width += $(this).width();
    });
    $(this.rootEl).width(width+5+30);
}
