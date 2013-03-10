// Copyright (C) projekt-und-partner.com, 2010
// Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

namespace("p2");

p2.PropertyForm = function(url, sourceId, setobjectId){
    // if (!setobjectId) throw new Error("PropertyForm constructor: setobjectId is obligatory!");
	var self = this;
	this.rootEl = $('<div></div>');
	this.isLoaded = false;
	this.setobjectId = setobjectId;
	this.sourceId = sourceId;
    console.log('setobjectId' + setobjectId); 
    var options = {
		autoOpen: false,
        closeOnEscape: true, // works together with close option, which resets form
		height: 370,
		width: 500,
		modal: true,
		open: function(event, ui){
            // we don't show the close icon for *this* dialog
            $(".ui-dialog-titlebar-close", $(this).parent()).hide();
        },
		title: 'Properties',
		close: function(event) {
			if (event.originalTarget != null){
				// the event stems not from a custom button 
				// which is defined through the "buttons" option
				// above. 
				// It must be an close event driven from "outside"
				// like pressing ESCape or the close icon.
                self.cancel();
			}
		}
	};
	this.dialog = $(this.rootEl).dialog(options);
    p2.Formloader.call(this, url, 'OPERATIONAL', sourceId, setobjectId);

	$(this.rootEl).bind('P2_CLOSE', function(e){
        self.close();
        return true;
	});
    $(this.rootEl).bind('P2_RESET', function(e){
        self.cancel();
        return true;
    });
}

p2.PropertyForm.prototype = function(){
    function instance(){};
	instance.prototype = p2.Formloader.prototype;
	return new instance();
}();

p2.PropertyForm.prototype.constructor = p2.Formloader;


p2.PropertyForm.prototype.open = function(success){
    var self = this;
    var _success = function(){
        self.isLoaded = true;
        if (success) success(arguments);
    }
    // If dialog is already there, we don't load it again from database
    if (!this.isLoaded){
        p2.Formloader.prototype.open.call(this, this.rootEl, _success);
    }
	$(this.dialog).dialog('open');
}

p2.PropertyForm.prototype.close = function(){
    $(this.dialog).dialog('close');
}

p2.PropertyForm.prototype.onOk = function(element){
    $(this.rootEl).find('.input').each(function(){
        // We have a new default value for the field,
        // since the user committed the current value!
        this.defaultValue = $(this).val();
    });
    this.close();
}

p2.PropertyForm.prototype.cancel = function(){
    var self = this;
    // reset field values with default values.
    $(this.rootEl).find('.p2-span').each(function(outer){
        var spanType = $(this).attr('data-span-type');
        $(this).find('.input').each(function(inner){
            if (spanType == 'checkbox'){
                if (this.defaultValue){
                    $(this).attr('checked', true);
                }else{
                    $(this).attr('checked', false);
                }
            }else{ 
                $(this).val(this.defaultValue);
            }
            // Trigger change event manually, as it is not user driven, but program driven.
            $(this).change();
        });
   });
}



