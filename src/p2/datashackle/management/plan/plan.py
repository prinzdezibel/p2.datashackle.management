# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2010
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok
import logging
import os
import types

import cssutils
from grokcore.content.interfaces import IContext
from sqlalchemy import orm
from zope.app.appsetup.product import getProductConfiguration
from zope.component import getUtility, queryUtility
from zope.location.interfaces import ILocation

from p2.datashackle.core import model_config
from p2.datashackle.core.app.exceptions import *
from p2.datashackle.core.app.setobjectreg import setobject_type_registry
from p2.datashackle.core.models.setobject_types import SetobjectType
from p2.datashackle.core.interfaces import ILocationProvider, IPlan, IDbUtility 
from p2.datashackle.management.form.form import FormType
from p2.datashackle.management.widget.widget import WidgetType
from p2.datashackle.management.span.span import SpanType

        
def fetch_plan(genericset):
    db_util = getUtility(IDbUtility)
    session = db_util.Session()
    plan = session.query(Plan).filter_by(plan_identifier=genericset.plan_identifier).one()
    session.add(plan)
    plan.make_locatable(genericset.__name__, genericset.__parent__)
    return plan

@model_config(tablename='p2_plan')
class Plan(SetobjectType):
    # In order to find default views via /index rather than
    # Zope3's /index.html we need to implement interfaces.IContext
    grok.implements(IPlan, IContext, ILocation)
 
    def __init__(self, id):
        self.id = id
        self.forms = dict()
        
        #util = getUtility(ILocationProvider)
        #genericset = util.get_genericset(objid)
        #self.table_identifier = genericset.table_identifier
        super(Plan, self).__init__()
        
    @orm.reconstructor          
    def reconstruct(self):
        util = getUtility(ILocationProvider)
        genericset = util.get_genericset(self.plan_identifier) # Requires that genericset.plan_identifier
                                                               # (yes, genericset.plan_identifier, not self.plan_identifier)
        if genericset != None:
            self.make_locatable(genericset.__name__, genericset.__parent__)
        #so_type = setobject_type_registry.get(self.so_module, self.so_type)
        #if so_type is not None:
        #    self.table_identifier = so_type.get_table_name()
        super(Plan, self).reconstruct()
    
    def common_init(self):
        super(Plan, self).common_init()
        self.form_type = FormType.__name__
        self.form_module = FormType.__module__
            
        config = getProductConfiguration("setmanager")
        style_dir = config.get('management_styles')
        self.stylesheet_name = str(self.id) + '.css'
        self.stylesheet_filepath = os.path.join(style_dir, self.stylesheet_name)
        self.stylesheet_exists = os.path.exists(self.stylesheet_filepath)
        if self.stylesheet_exists:
            self.stylesheet = cssutils.parseFile(self.stylesheet_filepath, encoding='utf-8')
        elif not hasattr(self, 'stylesheet'):
            self.stylesheet = cssutils.css.CSSStyleSheet()


    def set_default(self, form):
        self.default_form = form

    def make_locatable(self, name, parent):
         # Implementation of ILocation interface enables the object to be located with an URL,
         # which is needed for views of the plan, form and the like.
         self.__name__ = name
         self.__parent__ = parent
                 
    def register_form(self, form):
        if not form.form_name in self.forms:
            self.forms[form.form_name] = form
           
    def traverse(self, name):
        if name == 'forms':
            return FormDirectory(self)
        elif name == 'default_form':
            return self.default_form
    
    def is_archetype(self):
        """ Check whether we are an archetype plan."""
        if self.plan_identifier == 'p2_archetype':
            return True
        return False

    @property
    def table_identifier(self):
        """The table on which this plan is operating."""
        so_type = setobject_type_registry.lookup(self.so_module, self.so_type)
        return so_type.get_table_name()
 
    def update_css_rule(self, selector_text, value):
        declarations = value.split(';')
        for declaration in declarations:
            colon = declaration.find(':')
            if colon == -1:
                # nothing found
                continue
            css_name = declaration[:colon]
            css_value = declaration[colon + 1:]
            css_property = cssutils.css.Property(name=css_name, value=css_value)
            found = False
            # Check if selector already exists
            for css_rule in self.stylesheet.cssRules:
                if not isinstance(css_rule, cssutils.css.CSSStyleRule):
                    continue
                for selector in css_rule.selectorList:
                    if selector_text == selector.selectorText:
                        found = True
                        #css_rule.style[css_property] = css_value
                        css_rule.style.setProperty(css_property)
            if not found:
                declaration = cssutils.css.CSSStyleDeclaration()
                declaration.setProperty(css_property)
                #declaration[css_property] = css_value
                css_rule = cssutils.css.CSSStyleRule(
                    selectorText=selector_text,
                    style=declaration
                )
                self.stylesheet.add(css_rule)
    
    def write_stylesheet(self):
        cssfile = open(self.stylesheet_filepath, 'w+')
        cssfile.write(self.stylesheet.cssText)
        cssfile.close()
 

class FormDirectory(object):
    def __init__(self, plan):
        self.plan = plan
        self.forms = plan.forms


class FormTraverser(grok.Traverser):
    grok.context(FormDirectory)

    def traverse(self, name):
        if name in self.context.forms:
            return self.context.forms[name]
        raise Exception("Form does not exist.")

