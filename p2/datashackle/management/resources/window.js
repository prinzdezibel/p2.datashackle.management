// Copyright (C) : 	James Luterek
// 					projekt-und-partner.com, 2010
//
// Author:		James Luterek
// 				Michael Jenny <michael.jenny%40projekt-und-partner.com>

namespace("p2");

p2.Window = function(parentEl, windowId, openFn, options) {
	if ($(parentEl).length == 0) throw Error("Parent element does not exist.");
	var self = this;
	this.windowId = windowId;
	// Population of window is done through callback function.
	if (typeof(openFn) != 'function') throw new Error("Open function MUST be specified via openFn parameter.");
	this.openFn = openFn;
	this.defaults = {
		windowTitle : "",
		width : 200,
		height : 200,
		posx : 15,
		posy : 30,
		statusBar : true,
		minimizeButton : true,
		minimizeIcon : "-",
		maximizeButton : true,
		maximizeIcon : "&#926;",
		closeButton : true,
		closeIcon : "X",
		draggable : false,
		resizeable : true,
		resizeIcon : "&#8756;",
		overflow : 'auto',
		cssClass : '',
		initialHide: true,
	};
	
	$.extend(this.defaults, options);
	
	this.windowTitle = this.defaults.windowTitle;
			
	// This is our window DOM element.
	var $rootEl = $('<div class="window-container"><div class="window-back"></div></div>');
	this.rootEl = $rootEl.get(0);
    $(parentEl).append(this.rootEl);
	
	if (this.defaults.cssClass.length > 0){
		$rootEl.addClass(this.defaults.cssClass);
	}
	
	$(this.rootEl).data('window', this);
	var lastMouseX = 0;
	var lastMouseY = 0;
	var $windowTitleBar = $('<div class="window-titleBar"></div>');
	$windowMinimizeButton = $('<div class="window-minimizeButton">' + 
			this.defaults.minimizeIcon + '</div>');
	$windowMaximizeButton = $('<div class="window-maximizeButton">' +
			this.defaults.maximizeIcon + '</div>');
	if (this.defaults.closeButton){
		$windowCloseButton = $('<div class="ui-dialog-titlebar-close ' +
			'window-closeButton"><span>' + this.defaults.closeIcon + '</span></div>');
	}
	$windowContent = $('<div class="window-content"></div>');
	$windowStatusBar = $('<div class="window-statusBar"></div>');
	$windowResizeIcon = $('<div class="window-resizeIcon">' +
		this.defaults.resizeIcon + '</div>');	

	$(this.rootEl).bind('layerchange', function(event, position){
		// ignore events from myself
		if (event.target != self.rootEl){
			if (position == 'top'){
				self.bringToForeground();
			}else{
				self.moveToBackground();
			}
		}
	});

	if (this.defaults.draggable) {
		$rootEl.draggable({
			containment: 'parent',
			start: function(){
				// store position for drop event.
				$rootEl.data('pos', $rootEl.position());
				return p2.Window.prototype.bringToForeground.apply(self, arguments);
			}
		});
	}
	
	$windowMinimizeButton.bind('click', function(e) {
		p2.Window.prototype.fadeOut.apply(self, arguments);
		$(self.rootEl).trigger('visuality', [self, 'minimized']);
		// prevent event bubbling
		return false;
	});

	if (this.defaults.maximizeButton){
		$windowTitleBar.bind('dblclick', function(e) {
			$obj = $(e.target).parent();
			self.bringToForeground($obj);
			if ($obj.attr("state") == "normal") {
				$obj.animate( {
					top : "50px",
					left : "10px",
					width : $(window).width() - 65,
					height : $(window).height() - 75
				}, "slow");
				$obj.attr("state", "maximized")
			} else if ($obj.attr("state") == "maximized") {
				$obj.animate( {
					top : $obj.attr("lastY"),
					left : $obj.attr("lastX"),
					width : $obj.attr("lastWidth"),
					height : $obj.attr("lastHeight")
				}, "slow");
				$obj.attr("state", "normal")
			}
		});
		
		$windowMaximizeButton.bind('click', function(e) {
			$obj = $(e.target).parent().parent();
			self.bringToForeground($obj);
			if ($obj.attr("state") == "normal") {
				$obj.animate( {
					top : "50px",
					left : "10px",
					width : $(window).width() - 65,
					height : $(window).height() - 75
				}, "slow");
				$obj.attr("state", "maximized")
			} else if ($obj.attr("state") == "maximized") {
				$obj.animate( {
					top : $obj.attr("lastY"),
					left : $obj.attr("lastX"),
					width : $obj.attr("lastWidth"),
					height : $obj.attr("lastHeight")
				}, "slow");
				$obj.attr("state", "normal")
			}
		});
	};
	
	if (this.defaults.closeButton){
		$windowCloseButton.bind('click', function(e) {
			if (this.defaults.close != null) {
				var fn = this.defaults.close;
				fn.apply(arguments);
			}
		});
	}
	
	$windowContent.click(function(e) {
		self.bringToForeground($(e.currentTarget).parent());
	});
	$windowStatusBar.click(function(e) {
		self.bringToForeground($(e.currentTarget).parent());
	});
	this.move(this.defaults.posx, this.defaults.posy);
	$rootEl.attr("state", "normal");
	$windowTitleBar.append(this.defaults.windowTitle);

	if (this.defaults.minimizeButton)
		$windowTitleBar.append($windowMinimizeButton)
	if (this.defaults.maximizeButton)
		$windowTitleBar.append($windowMaximizeButton)
	if (this.defaults.closeButton)
		$windowTitleBar.append($windowCloseButton);
	if (this.defaults.resizeable){
		$windowStatusBar.append($windowResizeIcon);
	}

	$rootEl.append($windowTitleBar)
	$rootEl.append($windowContent)
	if (this.defaults.statusBar){
		$rootEl.append($windowStatusBar);
	}

	this.bindResizeEvent();
	
	if (this.defaults.initialHide == true) $rootEl.hide();
	
	$rootEl.bind('click', function(e) {
		$obj = $(e.currentTarget).parent();
		self.bringToForeground($obj);
	});

	this._createButtons($windowStatusBar, this.defaults.buttons);
	
    // Populate window through callback function.
	this.openFn($rootEl.children(".window-content"));

    // this.setWindowSize(self.defaults.width, self.defaults.height);

	if (!this.defaults.draggable)
		$rootEl.children(".window-titleBar").css("cursor", "default");
}

p2.Window.prototype.reload = function(){
    // Populate window through callback function.
	this.openFn($(this.rootEl).children(".window-content"));
}

p2.Window.prototype.bindResizeEvent = function(){
	if (this.defaults.resizeable){
		var self = this;
		var $windowResizeIcon = $(this.rootEl).find('.window-resizeIcon');
		var resizing = function(e, $obj) {
			e = e ? e : window.event;
			var w = parseInt($obj.css("width"));
			var h = parseInt($obj.css("height"));
			w = w < 200 ? 200 : w;
			h = h < 20 ? 20 : h;
			var neww = w + (e.clientX - lastMouseX);
 			var newh = h + (e.clientY - lastMouseY);
			lastMouseX = e.clientX;
			lastMouseY = e.clientY;

			self.setWindowSize(neww, newh);
		};
		
		$windowResizeIcon.bind('mousedown', function(e) {
			$obj = $(e.target).parents('.window-container');
			self.bringToForeground($obj);
	
			if ($obj.attr("state") == "normal") {
				e = e ? e : window.event;
				lastMouseX = e.clientX;
				lastMouseY = e.clientY;
	
	            var resizeFn = function(e) {
					resizing(e, $obj);
				};
				$(document).bind('mousemove', resizeFn);
	
				$(document).bind('mouseup', function(e) {
					$(document).unbind('mousemove', resizeFn);
					if (self.defaults.resizeCallback != null){
					    self.defaults.resizeCallback(self.getWindowSize());
					}
				});
			}
			// Prevent the drag handler from dragging the window. We are only
			// interested in resizing. For the curious:
			// http://stackoverflow.com/questions/1357118/javascript-event-preventdefault-vs-return-false
			return false;
		});
	}
}

p2.Window.prototype.move = function(x, y){
	$(this.rootEl).attr("lastX", x).attr("lastY", y).css("left", x).css("top", y);
}

p2.Window.prototype.setWindowSize = function(width, height) {
	$(this.rootEl).attr("lastWidth", width).
		attr("lastHeight", height);
		
		// send event that the size has changed
		$(this.rootEl).trigger('MSG_WINDOW_SIZE_CHANGED', [width, height]);
}

p2.Window.prototype.getWindowSize = function() {
	return {width: $(this.rootEl).width(),
		   height: $(this.rootEl).height()}
}

p2.Window.prototype._createButtons = function(container,	buttons) {
	var hasButtons = false;
	var uiDialogButtonPane = $('<div></div>')
			.addClass(
					'ui-dialog-buttonpane ' + 'ui-widget-content ' + 'ui-helper-clearfix');

	(typeof buttons == 'object' && buttons !== null && $.each(buttons,
			function() {
				return !(hasButtons = true);
			}));
	if (hasButtons) {
		$.each(buttons, function(name, fn) {
			$('<button type="button"></button>').addClass(
					'ui-state-default ' + 'ui-corner-all').text(name).click(
					function() {
						fn.apply(arguments);
					}).hover(function() {
				$(this).addClass('ui-state-hover');
			}, function() {
				$(this).removeClass('ui-state-hover');
			}).focus(function() {
				$(this).addClass('ui-state-focus');
			}).blur(function() {
				$(this).removeClass('ui-state-focus');
			}).appendTo(uiDialogButtonPane);
		});
		uiDialogButtonPane.appendTo(container);
	}
}

p2.Window.prototype.bringToForeground = function(){
	$(this.rootEl).trigger('layerchange', [this, 'top']);
}

p2.Window.prototype.moveToBackground = function(){
	$(this.rootEl).trigger('layerchange', [this, 'bottom']);
}

p2.Window.prototype.setZIndex = function(value){
	$(this.rootEl).css("z-index", value);
}

p2.Window.prototype.fadeIn = function(){
	$(this.rootEl).fadeIn();
    var size = this.getWindowSize();
    $(this.rootEl).trigger('MSG_WINDOW_SIZE_CHANGED', [size.width, size.height]);
}

p2.Window.prototype.fadeOut = function(){
	$(this.rootEl).fadeOut();
}
