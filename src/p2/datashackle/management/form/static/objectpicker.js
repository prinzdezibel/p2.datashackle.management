// Copyright (C) projekt-und-partner.com, 2011
// Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

namespace("p2");

p2.ObjectPicker = function(relationSourceId, relationId, isMultiSelectable, sourceId){
    if (!sourceId){debugger; throw Error("sourceId is mandatory.")}
    this.relationId = relationId;
  	this.rootEl = $('<div></div>');
    this.checkboxes = {};
    this.relationSourceId = relationSourceId;
    this.isMultiSelectable = isMultiSelectable;
    this.sourceId = sourceId;
    if (sourceId != null){
        this.linkageVertex = p2.datashackle.core.session.graph.lookupGraphObject(this.sourceId).vertex;
    }
}

p2.ObjectPicker.prototype.open = function(resource){
    var self = this;
    var options = {
		autoOpen: false,
        closeOnEscape: true, // works together with close option, which resets form
		height: 500,
		width: 700,
		modal: true,
		open: function(event, ui){},
		title: 'Edit objects',
        buttons: {'OK': function(){self.onOk.apply(self,[]);}},
		close: function(event) {
			if (event.originalTarget != null){
				// the event stems not from a custom button 
				// which is defined through the "buttons" option
				// above. 
				// It must be an close event driven from "outside"
				// like pressing ESCape or the close icon.
			}
			//first, find out the setobject id our table row form operates on
			span = $('div.p2-form[data-node-id="' + self.relationSourceId + '"]');
			tablerowform = span.parents('.outerstaticframe');
			id = tablerowform.find(' > div > .p2-form').attr('data-node-id');
			//get the form name
			formname = 'default_form';
			settings = p2.datamanagement.datarowsettings.getSettingsObject.apply(p2.datamanagement.datarowsettings, [id]);
            if (!settings.formname) {settings.formname = formname;}else{formname = settings.formname;}
            //mark form changed (it doesn't need to be, but assume that for now)
			p2.datamanagement.FormMarkChanged.apply(p2.datamanagement, [id]);
			//reload form (to update displayed collection contents)
			p2.datamanagement.ChangeToForm.apply(p2.datamanagement, [id, formname]);
			
		}
	};
	var dialog = $(this.rootEl).dialog(options);
	this.dialog = dialog;
	
	//mark the vertex we work on as changed (so it is sent to the server now in the graph and also later when we did our linkage modifications)
	var vertex = p2.datashackle.core.session.graph.queryGraphObject(this.relationSourceId).vertex;
	if (vertex.action == "ignore") {vertex.action = "save";}
	
	//assemble ajax request data
    var graph = p2.datashackle.core.session.graph.toXml(null); // submit all nodes
    this.data = {
        'relation_id': this.relationId,
        'relation_source_id': this.relationSourceId,
        'graph': graph,
        'mode': 'OPERATIONAL'
    };
    
    //fire off ajax request to get the object picker dialog's content
    $.ajax({url: resource + '/@@objectpicker',
            data: this.data,
            async: false,
            type: 'POST',
            timeout: 6000,
            success: function(contentHtml, textStatus, xhr){
                $(self.rootEl).html(contentHtml);
	            $(dialog).dialog('open');
            }
    });
}

p2.ObjectPicker.prototype.close = function(){
    this.dialog.dialog('close');
}

p2.ObjectPicker.prototype.onOk = function(element){
    this.close();
}

p2.ObjectPicker.prototype.onClick = function(el){
    var self = this;
    if (!this.isMultiSelectable){
        for (id in self.checkboxes){
            if (id != $(el).val()){
                self.setChecked(self.checkboxes[id], false);
            }
        }
    }
    this.setChecked($(el), $(el).is(':checked'));
}

p2.ObjectPicker.prototype.registerCheckbox = function($el, checked){
    var self = this;
	$el.bind('click', function(){
        return self.onClick(this);
    });
    var id = $el.val();
    this.checkboxes[id] = $el;
    // Value from client graph has precedence over the server values
    if (this.linkageVertex.hasLinkInfo(id)){
        this.setChecked($el, this.linkageVertex.isLinked(id));
    }else{
        this.setChecked($el, checked);
    }
}

p2.ObjectPicker.prototype.setChecked = function(el, checked){
    if (checked){
        $(el).attr('checked', 'checked');
        this.linkageVertex.link($(el).val());
    }else{
        $(el).removeAttr('checked');
        this.linkageVertex.unlink($(el).val());
    }
}
