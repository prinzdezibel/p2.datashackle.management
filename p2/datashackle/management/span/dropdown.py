# -*- coding:utf-8 -*-
# Copyright(C) projekt-und-partner.com, 2011
# Author: Michael Jenny

from sqlalchemy import orm
from zope.component import getUtility

from p2.datashackle.core import model_config
from p2.datashackle.core.app.exceptions import SetobjectGraphException
from p2.datashackle.core.app.setobjectreg import setobject_table_registry, setobject_type_registry
from p2.datashackle.core.interfaces import IDbUtility
from p2.datashackle.core.models.linkage import Linkage
from p2.datashackle.core.models.relation import Relation
from p2.datashackle.management.span.span import PolymorphicSpanType


@model_config(maporder=2)
class Dropdown(PolymorphicSpanType):
   
    width = 95
 
    def __init__(self, span_name=None):
        self.relation = Relation('MANY_TO_ONE')
        self.linkage = Linkage()
        # Set the linkage's relation to this form's relation
        self.linkage.relation = self.relation
        self.css = "left:" + str(self.label_width) + "px; width:" + str(self.width) + "px;"
        super(Dropdown, self).__init__(span_name)
    
    def onbefore_post_order_traverse(self, setobject, mode):
        if self.required == True and getattr(setobject, self.linkage.attr_name) is None and mode == 'save':
            raise SetobjectGraphException("Please select a value for '" + self.widget.spans['label'].span_value + "'.")

    def post_order_traverse(self, mode):
        if mode == 'save':
            from p2.datashackle.management.model.model import Model
            plan_id = self.plan_identifier
            session = Session()
            plan = session.query(Model).filter_by(plan_identifier=plan_id).one()
            source_type = self.op_setobject_type
            target_type = setobject_type_registry.lookup(plan.klass)
    
            # set relation value
            self.relation.source_table = source_type.get_table_name()
            self.relation.target_table = target_type.get_table_name()
            self.relation.create_relation('LIST')
            
            # Set computed linkage values
            self.linkage.source_model = plan
            m = session.query(Model).filter_by(klass=plan.klass).one()
            self.linkage.target_model = m
     
    def __setattr__(self, name, value):
        super(Dropdown, self).__setattr__(name, value)
        if name == 'linkage':
            if self.plan_identifier != None and value != None:
                # Get the table identifier from our plan identifier and set it as the linkage's target class
                table = setobject_table_registry.lookup_by_table('p2_model')
                plan = getUtility(IDbUtility).engine.execute(table.select(table.c.plan_identifier == self.plan_identifier)).first()
                plan_type = plan['so_type']
                table_identifier = setobject_type_registry.lookup(plan_type).get_table_name()
                oldtargetclass = None
                try:
                    oldtargetclass = self.linkage.target_classname
                except AttributeError:
                    pass
                if oldtargetclass == None or oldtargetclass == "":
                    self.linkage.target_classname = table_identifier
        
    def _get_info(self):
        info = {}
        if self.operational:
            info['linkage_id'] = self.linkage.id
            info['attr_name'] = self.attr_name
        return info


