// JavaScript Window Manager
// OS-like UI written in Javascript and jQuery
//
// Copyright (C) : 	James Luterek
//
// Author:		James Luterek
// 				Michael Jenny <michael.jenny%40projekt-und-partner.com>
//


namespace("p2");

p2.WindowManager = function(identifier, rootEl, options) {
	var self = this;
	this.name = identifier;
	this.rootEl = rootEl;
	this.windows = new Array();

	var defaults = {
		domContent : "",
		content : "",
		ajaxURL : false,
		iframeURL : ""
	};

	this.options = $.extend(defaults, options);

	if (p2.readCookie('bgColor') != null) {
		this.ChangeBGColor(p2.readCookie('bgColor'));
	}
	if (p2.readCookie('bgImage') != null) {
		this.ChangeBGImage(p2.readCookie('bgImage'));
	}
	if (p2.readCookie('themeColor') != null) {
		this.ChangeThemeColor(p2.readCookie('themeColor'));
	}
	if (p2.readCookie('themeTextColor') != null) {
		this.ChangeThemeTextColor(p2.readCookie('themeTextColor'));
	}

};

p2.WindowManager.zIndexBase = 100;


p2.WindowManager.onLayerChange = function(event, window, position){
	// **this** refers to the windowmanager instance
	var index = undefined;
	for (var i = 0; i < this.windows.length; i++){
		if (this.windows[i].window == window){
			if (position == 'top'){
				// move object to first position in stack
				this.windows.push(this.windows.splice(i, 1)[0]);
			}else if (position == 'bottom'){
				// move object to last position in stack
				this.windows.unshift(this.windows.splice(i, 1)[0]);
			}else{
				throw Error("Can't position window. Unknown layer.")
			}
			index = i;
			break;
		}
	}
	
	if (index != undefined){
		for (var i = 0; i < this.windows.length; i++){
			this.windows[i].window.setZIndex(p2.WindowManager.zIndexBase + i);
		}
		this.showWindow(this.windows[index]);
	}
}



p2.WindowManager.prototype.registerWindow = function(formName, window){
	var self = this;

	this.windows[formName] = window;
	
    $(document).bind('layerchange', function(){
		return p2.WindowManager.onLayerChange.apply(self, arguments);
	});
	
	
	
	// Default position is foreground (push)
	this.windows.push(window);
		
	//this.showWindow(window_and_button);

    return window;
}

p2.WindowManager.prototype.showWindow = function(window) {
	window.fadeIn();
};

p2.WindowManager.prototype.hideWindow = function(window) {
	window.fadeOut();
};

