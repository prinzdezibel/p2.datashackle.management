# -*- coding:utf-8 -*-
# Copyright(C) projekt-und-partner.com, 2011
# Author: Michael Jenny

from sqlalchemy import orm
from zope.component import getUtility

from p2.datashackle.core import model_config, Session
from p2.datashackle.core.app.setobjectreg import setobject_table_registry, setobject_type_registry
from p2.datashackle.core.app.exceptions import UserException
from p2.datashackle.core.interfaces import IDbUtility
from p2.datashackle.core.models.setobject_types import SetobjectType
from p2.datashackle.core.models.linkage import Linkage
from zope.component import getUtility

from p2.datashackle.core.app.setobjectreg import setobject_table_registry, setobject_type_registry
from p2.datashackle.management.span.span import SpanType


@model_config(tablename='p2_span_embeddedform', maporder=3)
class EmbeddedForm(SpanType):
    
    height = 50
    width = 50
 
    def __init__(self, span_name=None):
        self.linkage = Linkage()

        self.form_name = 'default_form'
        self.css_style = "left:" + str(self.label_width) + "px; width:" + \
            str(self.width) + "px; height:" + str(self.height) + "px;"
        super(EmbeddedForm, self).__init__(span_name)
   
    #def set_attribute(self, attribute, value, mode):
    #    super(EmbeddedForm, self).set_attribute(attribute, value, mode)
    #    if attribute == 'linkage':
    #        # Set computed linkage values
    #        value.source_module = self.__module__
    #        value.source_classname = self.__class__.__name__
    #        plan_id = self.plan_identifier
    #        session = Session()
    #        from p2.datashackle.management.plan.plan import Plan
    #        plan = session.query(Plan).filter_by(plan_identifier=plan_id).one()
    #        value.target_module = plan.so_module
    #        value.target_classname = plan.so_type
    #    elif attribute == 'relation':
    #        value.source_table = self.get_table_name()
    #        plan_id = self.plan_identifier
    #        session = Session()
    #        from p2.datashackle.management.plan.plan import Plan
    #        plan = session.query(Plan).filter_by(plan_identifier=plan_id).one()
    #        value.target_table = plan.get_table_name()

    def post_order_traverse(self, mode):
        if mode == 'save':
            from p2.datashackle.management.plan.plan import Plan
            plan_id = self.plan_identifier
            session = Session()
            plan = session.query(Plan).filter_by(plan_identifier=plan_id).one()
            source_type = self.op_setobject_type
            target_type = setobject_type_registry.lookup(plan.so_module, plan.so_type)
            
            # Set computed values on inner objects
            self.linkage.source_module = source_type.__module__
            self.linkage.source_classname = source_type.__name__
            self.linkage.target_module = plan.so_module
            self.linkage.target_classname = plan.so_type

            self.linkage.relation.source_table = source_type.get_table_name() 
            self.linkage.relation.target_table = target_type.get_table_name()            

            if self.characteristic.id == 'ADJACENCY_LIST':
                # Ensure given linkage id that identifies which relation
                # is used to represent the tree structure
                if not self.adjacency_linkage:
                    raise UserException("Missing value. For tree types the linkage id is mandatory.")

            if self.linkage.relation.cardinality.id != 'NONE':
                self.linkage.relation.create_relation(self.characteristic.id)

    def _get_info(self):
        info = {}
        if self.operational:
            info['linkage_id'] = self.linkage.id
        return info

    @classmethod
    def map_computed_properties(cls):
        cls.sa_map_dispose()
        embeddedform_table = setobject_table_registry.lookup_by_class(cls.__module__, cls.__name__)
        inherits = SpanType._sa_class_manager.mapper
        orm.mapper(EmbeddedForm,
                   embeddedform_table, # We want joined table inheritance for the embeddedform span (additional table for embeddedform specific fields)
                   inherits=inherits,
                   polymorphic_identity='embeddedform',
                   properties=cls.mapper_properties
                   )
        
