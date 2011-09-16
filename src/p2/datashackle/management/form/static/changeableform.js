// Copyright (C) projekt-und-partner.com, 2010
// Author:  Jonas Thiem <jonas.thiem%40projekt-und-partner.com>

namespace("p2");

p2.ChangeableForm = function(setobjectid) {
    if (/^\d+$/.test(setobjectid) == false) {throw "Setobject id contains non-digit characters";}
    self = this;
    this.setobjectid = setobjectid;
    var setobject_id = this.setobjectid;

    //handle marked as dirty and saving
    var dirtyhandler = function(e, dirtyid) {
        if (dirtyid == setobject_id) {
            p2.datamanagement.FormMarkChanged.apply(p2.datamanagement, [dirtyid]);
        }
    };
    $(document).bind('form-mark-dirty', dirtyhandler);

    //handle removing handlers and objects when saved
    var savehandler = function(e) {
        var settings = p2.datamanagement.datarowsettings.getSettingsObject.apply(p2.datamanagement.datarowsettings, [setobject_id]);
        if (settings.runtimecreated == true) {
            p2.datamanagement.DeleteClick.apply(p2.datamanagement, [setobject_id]);
        }else{
            $(document).trigger('form-delete', setobject_id);
        }
        settings.dirty = false;
    }
    $(document).bind('form-global-save', savehandler);
        
    //handle deletion
    var deletehandler = function(e, id, keepsettings) {
        if (id == setobject_id) {
            var settings = p2.datamanagement.datarowsettings.getSettingsObject.apply(p2.datamanagement.datarowsettings, [setobject_id]);
            if (settings.dirty == true) {
                //p2.datamanagement.FormMarkSaved.apply(p2.datamanagement, [setobject_id]);
                settings.dirty = false;
            }
            $(document).trigger('form-remove-handlers', id);
        }
    }
    $(document).bind('form-delete', deletehandler);
        
    //handle navigating away
    var navigateawayhandler = function(e) {
        var settings = p2.datamanagement.datarowsettings.getSettingsObject.apply(p2.datamanagement.datarowsettings, [setobject_id]);
        if (settings.runtimecreated == false) {
            $(document).trigger('form-remove-handlers', setobject_id);
        }
    }
    $(document).bind('form-navigate-away', navigateawayhandler);
    
    //handle navigating away
    var reverthandler = function(e) {
        var settings = p2.datamanagement.datarowsettings.getSettingsObject.apply(p2.datamanagement.datarowsettings, [setobject_id]);
        if (settings.runtimecreated == true) {
            p2.datamanagement.DeleteClick.apply(p2.datamanagement, [setobject_id]);
        }else{
            $(document).trigger('form-delete', setobject_id);
        }
        settings.dirty = false;
        $(document).trigger('form-remove-handlers', setobject_id);
    }
    $(document).bind('form-global-revert', reverthandler);
    
    //handle removing handlers
    var removehandlers = function(e, id) {
        if (id == setobject_id) {
            $(document).unbind('form-delete', deletehandler);
            $(document).unbind('form-mark-dirty', dirtyhandler);
            $(document).unbind('form-remove-handlers', removehandlers);
            $(document).unbind('form-navigate-away', navigateawayhandler);
            $(document).unbind('form-global-save', savehandler);
            $(document).unbind('form-global-revert', reverthandler);
            //remove our form object
            eval("changeableformobj_" + id + " = undefined;");
        }
    }
    $(document).bind('form-remove-handlers', removehandlers);
};

p2.ChangeableForm.prototype.initialize = function() {
    settings = p2.datamanagement.datarowsettings.getSettingsObject.apply(p2.datamanagement.datarowsettings, [this.setobjectid]);
    var node = p2.datashackle.core.session.graph.queryGraphObject(this.setobjectid);
    var settings = p2.datamanagement.datarowsettings.getSettingsObject.apply(p2.datamanagement.datarowsettings, [this.setobjectid]);
    
    //mark us dirty if required
    if (settings.dirty == true) {
        p2.datamanagement.FormMarkChanged.apply(p2.datamanagement, [this.setobjectid]);
    }
    
    
    //make sure new unchanged things stay marked as 'new'
    if (settings.runtimecreated == true) {
        node.vertex.action = 'new';
    }
        
    //set this setobject to ignore if it isn't new and unchanged
    if (settings.dirty != true && settings.runtimecreated != true && node.vertex.action != 'delete') {
        if (node.parent == null) { //only set this for normal (not embedded) forms
            node.vertex.action = 'ignore';
        }
    }
        
    //mark us for deletion if required
    if (node.vertex.action == 'delete') {
        $('tr[id="tablerowform_' + this.setobjectid + '"]').addClass('tobedeleted');
        $('tr[id="tablerowform_' + this.setobjectid + '"] .p2-form input').attr('disabled', 'disabled');
    }
};

p2.ChangeableForm.prototype.findChildren = function() {
    node = p2.datashackle.core.session.graph.queryGraphObject(this.setobjectid);
    // obtain the div for our form
    rootobj = $('div[id="changeableform_' + this.setobjectid + '"]');
    if (rootobj.length < 1) {throw "Changeable form div for the changeableform operating on " + this.setobjectid + " not found.";}
    // get all divs inside us that are changeable forms, but NOT nested changeable forms
    var childitems = $(rootobj).find('div[id^="changeableform_"]').filter(function(){
        var nestedparents = $(this).parent().closest('div[id^="changeableform_"]');
        if (nestedparents.length <= 0) {return true;}
        if ($(nestedparents[0]).attr('id') != rootobj.attr('id')) {
            //since closest gives us the closest and it isn't our root obj, it must be even closer -> nested
            return false; //we don't want nested things
        }
        return true;
    });
    // now obtain the changeable form js objects for all divs we found
    var changeableformlist = new Array();
    var i = 0;
    var str = "changeableform_";
    var strlen = str.length;
    while (i < childitems.length) {
        // Extract the id
        var id = $(childitems[i]).attr('id').substring(strlen);
        // try to obtain the js object
        if (window['changeableformobj_' + id] != undefined) {
            changeableformlist.push(window['changeableformobj_' + id]);
        }
        i++;
    }
    return changeableformlist;
};
