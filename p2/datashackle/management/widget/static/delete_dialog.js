// Copyright (C) projekt-und-partner.com, 2010
// Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

namespace("p2");

p2.DeleteDialog = function(parentEl, deleteFn){
    var self = this;
    this.parentEl = parentEl;
    var content = $('<div title="Delete widget?">' +
    	'<p>The widget will be permanently deleted. Are you sure?</p>' +
        '</div>'
        );
    $(this.parentEl).append(content);
    this.rootEl = content;
    var options = {
        resizable: false,
        autoOpen: false,
		height: 150,
		width: 250,
		modal: true,
		buttons: {
        	"Delete widget": function() {
        	    if (deleteFn != null) deleteFn();
				$(this).dialog('close');
			},
			"Cancel": function() {
				$(this).dialog('close');
			}
		}
	};
	this.dialog = $(this.rootEl).dialog(options);
}
