// Copyright (C) projekt-und-partner.com, 2010
// Author:  Jonas Thiem <jonas.thiem%40projekt-und-partner.com>

namespace("p2");

p2.Datamanagement = function(planurl, planidentifier, parentid)
{
    var self = this;
    this.planidentifier = planidentifier;
    this.plan_url = planurl;
    this.filtertimeouthandle = null;
    this.parentid = parentid;
    this.filterstring = "";
    this.page = 1;
    this.displayedresultscount = 0;
    this.datarowsettings = new p2.Datamanagement.Datarowsettings();
    
    $('#' + this.planidentifier + '\\.action\\.save').click(function(){
       var sess = p2.datashackle.core.session;
       var xml = sess.graph.toXml(null);
       var data = {};
       data['data'] = xml;
       data[$(this).attr('name')] = $(this).text();
       $.ajax({url: self.plan_url,
               async: false,
               dataType: "json",
               type: "POST",
               data: data,
               success: function(data, textStatus, xmlHttpRequest){
                   if (data.error !== undefined){
                       errorshown = true;
                       alert(data.error);
                   }else{
                       success = true;
                       p2.datashackle.core.session.graph.init(); //this will wipe out the graph
                            try{
                       $('.p2-form').each(function(){
                            var dataid = $(this).attr('data-node-id');
                            self.FormMarkSaved(dataid);
                       });
                            }catch(err){alert(err)}
                   }
               },
               error: function(xhr, text, error){
                   alert(error);
               }
       });
    });
}
p2.Datamanagement.prototype._ActivateFilterCallbackComplete = function(XMLHttpRequest, textStatus)
{
	if (textStatus != 'success'){
		$('#' + this.parentid).html('<tr><td colspan="2"><h1>Error.</h1><div id="searcherror">There was an error retrieving the server response. Error string: "' + textStatus + '"</div></tr></td>');
    }
}
p2.Datamanagement.prototype._ActivateFilterCallbackSuccess = function(responseText)
{
    this.displayedresultscount = 0;
    $(document).trigger('form-navigate-away'); //wipe out old handlers
    try{
    $('#' + this.parentid).html(responseText); // the js code of this template will increase p2.datamanagement.displayedresultscount
    }catch(ex){alert(ex.message);debugger;}
    if (this.displayedresultscount <= 0) {
        $('#' + this.parentid).html("<tr><td colspan='2'>Nothing found.</td></tr>");
        if (this.page > 1) {
            //we really should go back to page 1 in that case
            this.page = 1;
            this.ActivateFilter();
        }
    }
}
p2.Datamanagement.prototype._ChangeToFormCallback = function(dataid, html)
{
    $(document).trigger('form-remove-handlers', dataid);
    $('#formfilterbox_' + dataid).html(html);
}
p2.Datamanagement.prototype.ChangeToForm = function(dataid, newformname)
{
    //store the form we will use now:
    settings = this.datarowsettings.getSettingsObject(dataid);
    settings.formname = newformname;
    var data = {mode: 'OPERATIONAL'};

    if (dataid){
        data.setobject_id = dataid;
        data.graph = p2.datashackle.core.session.graph.toXml();
    }    

    //request new form from server
    requrl = this.plan_url + "/forms/" + newformname + "/@@changeableform";
    var referencetous = this;
    $.ajax({url: requrl,
        dataType: "text",
        type: "POST",
        async: false,
        cache: false, 
        data: data,
        success: function(responseText) {referencetous._ChangeToFormCallback(dataid, responseText);}
        }
    );
}
p2.Datamanagement.prototype.DetailsClick = function(dataid)
{
    //find out whether we need to change to the tabular or main form
    newform = "main_form";
    settings = this.datarowsettings.getSettingsObject(dataid);
    if (settings.formname == "main_form") {
        newform = "tabular_form";
    }
    //now change to that form
    this.ChangeToForm(dataid, newform);
}
p2.Datamanagement.prototype.CheckNewForm = function(dataid) { 
    //check whether a newly loaded tabular form should be in detail mode (if yes, then change to detail mode!)
    settings = p2.datamanagement.datarowsettings.getSettingsObject(dataid);
    if (!settings.formname || settings.formname == 'tabular_form') {return;} //everything ok
    //ok a non-tabular form is specified. load it:
    this.ChangeToForm(dataid, settings.formname);
}
p2.Datamanagement.prototype._ReplaceWithTablerowCallback = function(tableid, html) {
    $('#' + tableid).append(html);
}
p2.Datamanagement.prototype.AddTablerow = function(tableid) {
    //request the new row with ajax:
    requrl = this.plan_url + "/default_form/@@tablerowform";
    var self = this;
    $.ajax({url: requrl,
        dataType: "text",
        type: "POST",
        async: false,
        cache: false, 
        data: {mode: 'OPERATIONAL',
               runtimecreated: 'true',
               setobject_id: ''
              },
        success: function(responseText) {self._ReplaceWithTablerowCallback(tableid, responseText);}
        }
    );
}

p2.Datamanagement.prototype.ActivateFilter = function()
{
    // Send a request to the search backend view
    requrl = this.plan_url + "/@@searchbackend";
    graph = p2.datashackle.core.session.graph.toXml();
    $.ajax({url: requrl,
            dataType: "text",
            type: "POST",
            async: false,
            cache: false, 
            context: this,
            data: {q: $('#searchfield').val(),
                   p: this.page
                  },
            complete: this._ActivateFilterCallbackComplete,
            success: this._ActivateFilterCallbackSuccess
            }
    );
}
p2.Datamanagement.prototype.FormMarkChanged = function(dataid)
{
    node = p2.datashackle.core.session.graph.queryGraphObject(dataid);
    if (node.vertex.action == "delete") {
        return;
    }
    // Sets a form dirty. Returns 'true' if the form was NOT dirty yet, 'false' if nothing changed (form was already dirty)
    var returnval = true;
    //set dirty flag
    settings = this.datarowsettings.getSettingsObject.apply(this.datarowsettings, [dataid]);
    if (settings.dirty == true) {returnval = false;}
    settings.dirty = true;
    //colour the form background
    $('#changeableform_' + dataid).addClass('resultstable_marked');
    //enable the global save button just in case it's not done yet
    //set setobject action to save
    if (node.vertex.action == "ignore") {
        node.vertex.action = "save";
    }
    return returnval;
}
p2.Datamanagement.prototype.FormMarkSaved = function(dataid)
{
    //remove dirty flag
    settings = this.datarowsettings.getSettingsObject(dataid);
    settings.dirty = false;
    //remove coloured form background
    $('#changeableform_' + dataid).removeClass('resultstable_marked');
    //set setobject action to ignore
    if (p2.datashackle.core.session.graph.queryGraphObject(dataid).vertex.action != "delete") {
        p2.datashackle.core.session.graph.queryGraphObject(dataid).vertex.action = 'ignore';
    }
}
p2.Datamanagement.prototype.NextPage = function(dataid)
{
    //advance one page
    this.page += 1;
    //reload page
    this.ActivateFilter();
}
p2.Datamanagement.prototype.PreviousPage = function(dataid)
{
    //advance one page
    this.page -= 1;
    //reload page
    this.ActivateFilter();
}
p2.Datamanagement.prototype.FormMarkRuntimecreated = function(dataid, domparentid)
{
    //mark this as runtime created and remember the id of the dom parent to delete it lateron.
    settings = this.datarowsettings.getSettingsObject(dataid);
    settings.runtimecreated = true;
    settings.runtimecreated_parentid = domparentid;
    //add coloured form background (since runtime created means not persisted yet)
    $('#formfilterbox_' + dataid).addClass('resultstable_marked');
    //set setobject action to save
    p2.datashackle.core.session.graph.queryGraphObject(dataid).vertex.action = "new";
}


p2.Datamanagement.prototype.DeleteClick = function(dataid)
{
    //check whether this is a runtime-created or server-loaded form
    settings = this.datarowsettings.getSettingsObject(dataid);
    if (settings.runtimecreated == true) {
        //remove the DOM tree element that contains the form row
        $('tr[id="tablerowform_' + dataid + '"]').remove();
        //remove handlers
        $(document).trigger('form-delete', dataid); //will wipe out some event handlers
        //remove setobject
        p2.datashackle.core.session.deleteNode.apply(p2.datashackle.core.session, [dataid]); //the whole setobject node
        //and of course the setobject as well as the settings
        settings = undefined; //dispose our reference (not sure if this is needed, but just in case)
        $(document).trigger('form-revert', dataid); //will delete the label things for us
        this.datarowsettings.deleteSettingsObject(dataid); //remove settings
        return;
    }else{
        //we need to tell the server that we want to delete it and then reload the page
        setobjectnode = p2.datashackle.core.session.graph.queryGraphObject(dataid);
        setobjectnode.vertex.action = "delete";
        //remove coloured form background if there is any
        $('#formfilterbox_' + dataid).removeClass('resultstable_marked');
        //mark the dom node as to be deleted
        $('tr[id="tablerowform_' + dataid + '"]').addClass('tobedeleted');
        $('tr[id="tablerowform_' + dataid + '"] .p2-form input').attr('disabled', 'disabled');
        //enable the global save button just in case it's not done yet
        settings.dirty = false;
    }
}
p2.Datamanagement.prototype.SetFilter = function(filter)
{
    if (this.filtertimeouthandle != null)
    {
        clearTimeout(this.filtertimeouthandle);
    }
    this.filterstring = filter;
    var referencetous = this;
    this.filtertimeouthandle = setTimeout(function(){
        referencetous.ActivateFilter.apply(referencetous, arguments);}, 800 );
}
p2.Datamanagement.Datarowsettings = function()
{
    this.storage = new function(){};
    // storage is an JS object (with no particular pre-defined functionality).
    // Settings are kept as "this.storage.settings_<primary key>" in a primary key-specific JS object.
    // Therefore it is NOT possible to cycle through all settings easily (without also going through
    // all other sorts of attributes that might reside on the this.storage object for various reasons).
    // If that should ever turn out to be necessary, I'll rewrite this to be a proper array instead.
}
p2.Datamanagement.Datarowsettings.prototype.getSettingsObject = function(primarykeyvalue)
{
    // This is the settings object. Simply store settings by placing .setting attributes on it.
    var obj = this.storage['settings_' + primarykeyvalue];
    if (!obj) {
        this.storage['settings_' + primarykeyvalue] = new function(){};
        obj = this.storage['settings_' + primarykeyvalue];
    }
    return obj;
}
p2.Datamanagement.Datarowsettings.prototype.deleteSettingsObject = function(primarykeyvalue)
{
    delete this.storage['settings_' + primarykeyvalue];
}
