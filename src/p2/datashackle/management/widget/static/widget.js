// Copyright (C) projekt-und-partner.com, 2010
// Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

namespace("p2.Widget");

p2.Widget = function(element, operational, propertyform, sourceId, type, dataNodeId, action, archetype, no_metaedit){
    var self = this;
    this.rootEl = element;
    this.operational = operational;
    this.sourceId = sourceId;
    this.type = type;
    this.dataNodeId = dataNodeId;
    this.action = action;

    if (!this.operational && archetype != "True"){
       var dataNode = p2.datashackle.core.session.registerDataNode(this.type, this.dataNodeId, this.action);
       var coll = p2.datashackle.core.session.graph.lookupGraphObject(this.sourceId).vertex;
       coll.link(this.dataNodeId);
    }

    this.widget_type = $(this.rootEl).attr('data-widget-type');
    
    if ($(this.rootEl).parents().is('#designerpage')){
        this.makeDraggable();
    }
    if ($(this.rootEl).parents().is('#view_area')){
        this.doDesignerEnhancements();
    }
  
    if (!no_metaedit){ 
        // append propertyform and bind it to edit button
        $(this.rootEl).append(propertyform);
        this.bindPropertyform(propertyform);
    }

    // Bind width change event
    $(this.rootEl).bind('MSG_SIZE_CHANGE', function(ev, width, height){
        self.calcWidth();
        return true;
    });
    
    this.bindDeleteDialog();    
}

p2.Widget.prototype.calcWidth = function(){
    var width = 0;
    $(this.rootEl).children('.p2-span').each(function(){
        width += $(this).width();
    });
    $(this.rootEl).width(width);
}

p2.Widget.prototype.bindPropertyform = function(propertyform){
    var label = $(this.rootEl).find('.anchor-edit');
    if (label.length != 0){
        $(label).click(function(){
            try {
                propertyform.open();
                // prevent default action
            }catch(e){
                alert("error: " + e);
            }
            return false;
        });
    }
}

p2.Widget.prototype.bindDeleteDialog = function(){
    var self = this;
    var anchor = $(this.rootEl).find('.anchor-delete');
    if (anchor.length != 0){
        var deleteDialog = new p2.DeleteDialog(anchor, function(){self.deleteWidget.call(self);});
        $(anchor).click(function(){
            p2.setdesigner.changed.apply(p2.setdesigner, []);
            try{
                deleteDialog.dialog.dialog('open');
            }
            catch (exc){
                throw exc
            }
            finally{
                return false;                
            }
        });
    }
}

p2.Widget.prototype.deleteWidget = function(){
    var node = p2.datashackle.core.session.graph.queryGraphObject(this.dataNodeId);
    var vertex = node.vertex;

    if (vertex.action == 'new'){
        // The item was new and now it's going to be deleted before it's going to database.
        // Don't push it to server, otherwise it tries to delete a widget which isn't in the db at all.
        p2.datashackle.core.session.deleteNode(this.dataNodeId);
    }else{
        vertex.setAction('delete');
        node.parent.vertex.unlink(this.dataNodeId);
    }
        
    $(this.rootEl).remove();
}

p2.Widget.prototype.setDirty = function(){
    $(this.rootEl).attr('data-action', 'save');
    // Inform others about the change
    $(this.rootEl).trigger('widget_change');
}


p2.Widget.prototype.makeDraggable = function(){
    var self = this;
    
    if ($(this.rootEl).parents().is('#toolbox')){
        var revert = true;
    }else{
        var revert = 'invalid';
    }
    
	$(this.rootEl).draggable({
		revert: revert,
		helper: 'original',
		scroll: false,
		cancel: '', // this is necessary. otherwise one will not be able to move textareas that catches the focus when dragging the widget
		/* grid: [15, 15], */
		// cursor: 'move',
		start: function() {
			//return p2.Widget.startDragging.apply(self, arguments);
		},
		drag: function(event, ui){self.calcWidth();},
		stop: function(event, ui){self.adaptCssValue(ui.helper);}
	});
}

p2.Widget.prototype.doDesignerEnhancements = function(){
	// ** this ** refers to the widget instance
	var self = this;
	
	// register float toggle function
	$(this.rootEl).find('.float-toggle').css('display', 'block');
	$(this.rootEl).find('.float-toggle').bind('click',
		function(event){$(this).toggle(
				p2.Widget.nofloat,
				p2.Widget.float
	)});
	
	// call toggle function for initializing
	$(this.rootEl).find('.float-toggle').click();
}


p2.Widget.startDragging = function(ev, ui) {
	// ** this ** refers to the widget instance
	//
	// The window where the dragging originates should be put
	// into foreground so that widgets can be moved to other
	// windows, if desired.
	
    // Moved widgets are marked for later update.
    this.setDirty();
    
	// does not work, because event is not triggered before this 
	// very own event has finished (dragging).
	$(this.rootEl).trigger('layerchange', ['top']);
	
	// for moving associated widgets when I'm moving.
	$(ui.helper).data('pos', $(ui.helper).position());
	
	offset = $(ui.helper).offset();
	p2.Widget.selected =
		$('.p2-widget.ui-selected').each(function() {
			$(this).data("offset", $(this).offset());
		});
}



p2.Widget.prototype.initCssPosition = function(rootEl, archetypeEl, archetypeOffset){

    // copy over initial css styles
    $(archetypeEl).find('.p2-span').each(function(index, sourceEl){
        var targetEl = $(rootEl).find('.p2-span')[index];
        $(targetEl).css({
            width: $(sourceEl).css('width'),
            height: $(sourceEl).css('height'),
            left: $(sourceEl).css('left')
        });
        var span = $(targetEl).data('data-object');
        span.setobject.setAttr('css', $(targetEl).attr('style'));
    });

	var archetypeId = $(archetypeEl).attr('id');
	if($(rootEl).parents().is('.window-container')){
		var windowPos = $(rootEl).parents('.window-container').offset();
	}else{
		throw new Error("Unknown droppable.");
	}
	
	var delta_x = archetypeOffset.left - windowPos.left;
	var delta_y = archetypeOffset.top - windowPos.top;
    	
	// round to nearest multiple of 15 (grid interval)
	var left = 15 * Math.round((delta_x) / 15);
	var top = 15 * Math.round((delta_y) / 15);
	
	$(rootEl).css({'position': 'absolute',
                 'overflow': 'visible',
                 'top': top + 'px',
                 'left': left + 'px'
                 });
    this.adaptCssValue(rootEl);
}

p2.Widget.prototype.adaptCssValue = function(element){
    this.calcWidth();
    var sourceId = $(element).attr('data-source-id');
    var style= $(element).attr('style');
    if (!this.operational){
        var setobject = p2.datashackle.core.session.registerDataNode(this.type, this.dataNodeId, this.action);
        setobject.setAttr('css', style);
    }
}



/* static methods */

p2.Widget.appendNew = function(element, archetypeEl, form){
    if (form == null){debugger; throw Error("Form object must be passed in.");}
    $(document).trigger('global-mark-dirty');
    sourceId = form.collectionId;
    formId = form.setobjectId;
    var archetypeId = $(archetypeEl).attr('data-widget-identifier');
    var widgetUrl = 'configuration/meta/p2_archetypes/forms/archetypes/' + archetypeId + '/@@archetypewidget';

    var vertex = p2.datashackle.core.session.graph.findRootVertex(sourceId);
    var graph = p2.datashackle.core.session.graph.toXml(formId);
    var data = {graph: graph};
    
    
        
    // When offset is passed as function parameter the ajax call can be asynchronous.
    // Otherwise the archetype would have already returned to its origin position. Offset
    // calculation of the newly created widget is then not possible.
    var archetypeOffset = $(archetypeEl).offset();
    $.ajax({url: widgetUrl, // It's important that the environment is set up with <base> tag.
            dataType: "text",
            type: "POST",
            async: true,
            timeout: 6000,
            data: {'source_id': sourceId,
                   'setobject_id': '',
                   'linked': 'true',
                   'graph': graph,
                   'mode': 'DESIGNER'
                  },
            success: function(contentHtml, textStatus, xhr){
                // Append it to DOM document.
                var $contentHtml = $(contentHtml);
                $(element).append($contentHtml);

                // We need to position the newly created widget.
                var widget = $contentHtml.data('data-object');
                widget.initCssPosition($contentHtml, archetypeEl, archetypeOffset);
                
                }   
            });
}

p2.Widget.float = function()
{
	$(this).next().css({'clear' : 'none'});
	$(this).removeClass('nofloat');
}

p2.Widget.nofloat = function()
{	
	$(this).next().css({'clear' : 'left'});
	$(this).addClass('nofloat');
}

