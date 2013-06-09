# -*- coding:utf-8 -*-
# Copyright(C) projekt-und-partner.com, 2011
# Author: Michael Jenny

from sqlalchemy import orm
from zope.component import getUtility

from p2.datashackle.core import model_config, Session
from p2.datashackle.core.app.setobjectreg import setobject_table_registry, setobject_type_registry
from p2.datashackle.core.app.exceptions import UserException
from p2.datashackle.core.interfaces import IDbUtility
from p2.datashackle.core.models.cardinality import Cardinality
from p2.datashackle.core.models.linkage import Linkage
from zope.component import getUtility

from p2.datashackle.core.app.setobjectreg import setobject_table_registry, setobject_type_registry
from p2.datashackle.management.span.span import PolymorphicSpanType


@model_config(maporder=3)
class EmbeddedForm(PolymorphicSpanType):
    
    height = 50
    width = 50
 
    def __init__(self, span_name=None):
        session = Session()
        self.linkage = Linkage()
        self.linkage.relation.cardinality = session.query(Cardinality). \
            filter(Cardinality.id == 'NONE').one()
        self.form_name = 'default_form'
        self.css = "left:" + str(self.label_width) + "px; width:" + \
            str(self.width) + "px; height:" + str(self.height) + "px;"
        super(EmbeddedForm, self).__init__(span_name)

    @orm.reconstructor          
    def reconstruct(self):
        if not self.linkage:
            # archetype embeddedform widget has no linkage object
            self.linkage = Linkage()   

    def post_order_traverse(self, mode):
        if mode == 'save':
            from p2.datashackle.management.plan.plan import Model
            plan_id = self.plan_identifier
            session = Session()
            plan = session.query(Model).filter_by(plan_identifier=plan_id).one()
            source_type = self.op_setobject_type
            target_type = setobject_type_registry.lookup(plan.klass)
            
            # Set computed values on inner objects
            m = session.query(Model).filter_by(klass=source_type.__name__).one()
            self.linkage.source_model = m
            m = session.query(Model).filter_by(klass=plan.klass).one()
            self.linkage.target_model = m

            self.linkage.relation.source_table = source_type.get_table_name() 
            self.linkage.relation.target_table = target_type.get_table_name()            

            if self.linkage.relation.cardinality.id != 'NONE':
                self.linkage.relation.create_relation()

    def _get_info(self):
        info = {}
        if self.operational:
            info['linkage_id'] = self.linkage.id
        return info

