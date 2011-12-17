// Copyright (C) projekt-und-partner.com, 2011
// Author:  Jonas Thiem <jonas.thiem%40projekt-und-partner.com>

namespace("p2");

p2.RelationPropertyform = function(propertyformSchemeHostPath, propertyFormSourceId, propertyformSetobjectId)
{
    p2.PropertyForm.call(this, propertyformSchemeHostPath, propertyFormSourceId, propertyformSetobjectId);
}

p2.RelationPropertyform.prototype = function()
{
    function instance(){};
	instance.prototype = p2.PropertyForm.prototype;
	return new instance();
}();

p2.RelationPropertyform.prototype.constructor = p2.PropertyForm;


p2.RelationPropertyform.prototype.open = function()
{
    // If dialog is already there, we don't load it again from database
    if (!this.isLoaded){
        var self = this;
        p2.Formloader.prototype.open.call(this, this.rootEl, function(){self.isLoaded = true; self.initialize();}, this.sourceId);
    }else{
        //this.formLoadedCallback(); //reissue shown event
    }
	$(this.dialog).dialog('open');
}

p2.RelationPropertyform.prototype.initialize = function()
{
    var widget = this.getplaninput();
    var cardinalitywidget = this.getcardinalityinput();
    var self = this;
    self.cardinalityvalue = self.getcardinalityvalue();
    self.planvalue = widget.val();
    if (widget.length && cardinalitywidget.length) {
        var func = function(e) {self.tablenamechangedfunc();};
        widget.bind('change', func);
        widget.bind('keydown', func);
        widget.bind('keyup', func);
        widget.bind('blur', func);
        cardinalitywidget.bind('change', func);
        cardinalitywidget.bind('keydown', func);
        cardinalitywidget.bind('keyup', func);
        cardinalitywidget.bind('blur', func);
    }

    //ok, let's fetch the list of plan identifiers and their respective table identifiers
    self.plan_table_list = undefined;
    
    $.ajax({url:p2.setdesigner.applicationUrl + "/@@jsoninfoquery" ,
        async: false,
        dataType: "json",
        type: "GET",
        success: function(data, textStatus, xmlHttpRequest){
            self.plan_table_list = data;
        }
    });
}

p2.RelationPropertyform.prototype.getcardinalityinput = function()
{
    return $(this.rootEl).find('div[data-field-identifier="cardinality"] > .input');
}

p2.RelationPropertyform.prototype.getplaninput = function()
{
    return $(this.rootEl).find('div[data-field-identifier="plan_identifier"] > .input');
}

p2.RelationPropertyform.prototype.getforeignkeyinput = function()
{
    return $(this.rootEl).find('div[data-field-identifier="foreignkeycol"] > .input');
}

p2.RelationPropertyform.prototype.getforeignkey2input = function()
{
    return $(this.rootEl).find('div[data-field-identifier="foreignkeycol2"] > .input');
}

p2.RelationPropertyform.prototype.getmappinginput = function()
{
    return $(this.rootEl).find('div[data-field-identifier="attr_name"] > .input');
}

p2.RelationPropertyform.prototype.gettargetforminput = function()
{
    return $(this.rootEl).find('div[data-field-identifier="form_name"] > .input');
}

p2.RelationPropertyform.prototype.getxreftableinput = function()
{
    return $(this.rootEl).find('div[data-field-identifier="xref_table"] > .input');
}

p2.RelationPropertyform.prototype.setwidgetvalue = function(widget, newvalue)
{
    widget().val(newvalue);
}
p2.RelationPropertyform.prototype.getcardinalityvalue = function() {
    var inputwidget = this.getcardinalityinput();
    return inputwidget.find(":selected").text();
}
p2.RelationPropertyform.prototype.tablenamechangedfunc = function()
{
    var self = this;
    var newcardinalityvalue = this.getcardinalityvalue();
    var newplanvalue = this.getplaninput().val();
    if (newcardinalityvalue == this.cardinalityvalue && newplanvalue == this.planvalue) {return;}
    self.cardinalityvalue = newcardinalityvalue;
    self.planvalue = newplanvalue;
    
    var cardinality = newcardinalityvalue.split(':');
    var othertable = undefined;
    var newfkvalue = undefined;
    var newfk2value = undefined;
    var owntable = p2.setdesigner.table_identifier;
    var xreftablename = "";
    
    //get the table identifier of the target plan specified
    if (self.plan_table_list != undefined) {
        othertable = self.plan_table_list[newplanvalue];
    }

    //check whether the input is sufficient to do meaningful auto filling
    var doautofill = false;
    if (cardinality.length == 2 && othertable != undefined) {
        doautofill = true;
    }
    
    if (doautofill) {
        //calculate auto fill values
        if (cardinality[0] == '1' && (cardinality[1] == '1(fk)' || cardinality[1] == 'n')) {
            //fk will be on other side referencing to us
            newfkvalue = "fk_" + owntable;
        }else{
            if (cardinality[1] == '1' && (cardinality[0] == '1(fk)' || cardinality[0] == 'n')) {
                //fk will be on our side referencing over there
                if (othertable != undefined) {
                    newfkvalue = "fk_" + othertable;
                }
            }else{
                if (newcardinalityvalue == 'n:m') {
                    // n:m relation
                    newfkvalue = "fk_" + owntable;
                    if (othertable != undefined) {
                        newfk2value = "fk_" + othertable;
                        var xrefpart = new Array();
                        xrefpart[0] = owntable;
                        xrefpart[1] = othertable;
                        xrefpart.sort();
                        xreftablename = xrefpart[0] + "_" + xrefpart[1];
                    }
                }
            }
        }
        
        //fill new values
        if (newfkvalue != undefined) {
            this.getforeignkeyinput().val(newfkvalue);
        }
        if (newfk2value != undefined) {
            this.getforeignkey2input().val(newfk2value);
        }
        if (othertable != undefined) {
            this.getmappinginput().val(othertable);
        }
        if (xreftablename != undefined) {
            this.getxreftableinput().val(xreftablename);
        }
        //trigger change events to update graph objects
        this.getforeignkeyinput().trigger('blur');
        this.getforeignkey2input().trigger('blur');
        this.getmappinginput().trigger('blur');
        this.getxreftableinput().trigger('blur');
    }
}


