// Copyright (C) projekt-und-partner.com, 2010
// Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

namespace("p2");

p2.DesignerFormresetDialog = function(parentEl, deleteFn){
    var self = this;
    this.parentEl = parentEl;
    var content = $('<div title="Reset form?">' +
    	'<p>Unsaved changes will be lost. Are you sure?</p>' +
        '</div>'
        );
    $(this.parentEl).append(content);
    this.rootEl = content;
    var options = {
        resizable: false,
        autoOpen: true,
		height: 150,
		width: 250,
		modal: true,
		buttons: {
        	"Reset form": function() {
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
