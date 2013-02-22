# -*- coding: utf-8 -*-
# Copyright (C), projekt-und-partner.com, 2011
# Author: Michael Jenny

import sqlalchemy.types
from sqlalchemy import func, Table
from sqlalchemy.sql import or_, not_, and_, desc
from sqlalchemy.sql.expression import case, column, literal_column, select
from sqlalchemy.orm import aliased
from zope.component import getUtility, getMultiAdapter

from p2.datashackle.core.globals import metadata
from p2.datashackle.core.app.setobjectreg import setobject_type_registry
from p2.datashackle.core.interfaces import IDbUtility
from p2.datashackle.management.span.embeddedform import EmbeddedForm
from p2.datashackle.management.interfaces import ILocationProvider



class QueryMode(object):
    """Specify the relation items that are honored in the query returned from a query()
       call on a RelationMixin."""
    SHARED = 1 # Honor all entries from target table
    EXCLUSIVE = 2 # Honor only entries from target table that are linked to current setobject
    WITH_UNLINKED = 3 # Honor EXCLUSIVE entries AND target table entries that are NULL (e.g. not linked yet)
    

class RelationMixin(object):
    """View mixin that requires that self.relation_source and self.relation are populated when calling its methods,
       whereas self.relation is the relation widget this is used on and self.relation_source the setobject the widget
       operates on."""
    
    # The id of the linkage which is used to determine related items
    collection_id = None

    def __init__(self, show_strip):
        self.show_strip = show_strip
 
    def update(self):
        self.is_multi_selectable = self.relation.linkage.relation.cardinality.id == 'ONE_TO_MANY'
        try:
            self.collection_id = self.relation_source.collections[self.relation.linkage.attr_name]['collection_id']
        except KeyError:
            raise Exception("Attribute %s does not exist on object %s. Check "\
                "if form_id of embeddedform_widget is matching the linkage " \
                "id." % (self.relation.linkage.attr_name, self.relation_source))


    def query_not_joined(self):
        session = getUtility(IDbUtility).Session()
        plan_id = self.relation.plan_identifier
        from p2.datashackle.management.plan.plan import Plan
        plan = session.query(Plan).get(plan_id)
        target_type = setobject_type_registry.lookup(plan.klass)        
        query = session.query(target_type)
        query = query.add_column(
            literal_column("'false'").label('linked')
        )
        if self.relation.characteristic.id == 'ADJACENCY_LIST':
            # Initially, only the root node(s) of embedded form is displayed.
            # Children are loaded on demand via Ajax.
            # Find root node(s) of tree
            linkage_id = self.relation.adjacency_linkage
            from p2.datashackle.core.models.linkage import Linkage
            linkage = session.query(Linkage).get(linkage_id)
            query = query.filter(getattr(target_type, linkage.relation.foreignkeycol) == None)
        if self.relation.filter_clause:
            query = query.filter(self.relation.filter_clause)
        return query


    def query_joined(self, query_mode):
        if query_mode == None:
            if self.relation.linkage.cardinality.id == 'ONE(FK)_TO_ONE' or \
                    self.relation.linkage.cardinality.id == 'ONE_TO_ONE(FK)':
                query_mode=QueryMode.WITH_UNLINKED
            else:
                query_mode=QueryMode.SHARED

        source_type = setobject_type_registry.lookup(self.relation.linkage.source_model.klass)
        target_type = setobject_type_registry.lookup(self.relation.linkage.target_model.klass)        
        session = getUtility(IDbUtility).Session()

        if target_type == source_type:
            target_type = aliased(source_type)        

        # Check if it is an xref relation
        xref_object = None
        if self.relation.linkage.cardinality.id == 'MANY_TO_MANY':
            xref_object = setobject_type_registry.lookup_by_table(self.relation.linkage.xref_table)
                
        # Compose query for various modes:
        if query_mode == QueryMode.SHARED:
            query = session.query(target_type)
            
            # For n:m, we need to outerjoin the xref table first:
            if not xref_object == None:
                query = query.outerjoin((xref_object,
                    target_type.get_primary_key_attr() == getattr(xref_object, self.relation.linkage.relation.foreignkeycol2)
                ))
            
            # Simply join with our source table from the target table. The join condition ensures we either get linked elements, or the source table's primary key field will be null/None.
            if xref_object == None:
                if self.relation.linkage.cardinality.id == 'ONE_TO_MANY' or \
                        self.relation.linkage.cardinality.id == 'ONE_TO_ONE(FK)':
                    joincondition = getattr(source_type,source_type.get_primary_key_attr_name()) == getattr(target_type, self.relation.linkage.relation.foreignkeycol)
                else:
                    joincondition = getattr(source_type,self.relation.linkage.relation.foreignkeycol) == target_type.get_primary_key_attr()
            else:
                joincondition = getattr(source_type,source_type.get_primary_key_attr_name()) == getattr(xref_object, self.relation.linkage.relation.foreignkeycol)
            
            query = query.outerjoin((source_type, joincondition))
            
            # Since the the source table's primary key is either filled for linked elements or None for unlinked, this simple condition to find out what is linked to ourselves is sufficient.
            # Unlinked entries won't match since their source primary key field will be None.
            query = query.add_column(
                func.max(
                    case([
                        (getattr(source_type, source_type.get_primary_key_attr_name()) == self.relation_source.id, 'true'),
                    ], else_='false')
                ).label('linked')
            )
            
            # For 1:n/1:1(fk), don't allow entries linked to someone else to show up (since they cannot have their foreign key point at two things).
            if xref_object == None and (
                    self.relation.linkage.cardinality.id == 'ONE_TO_MANY' or \
                    self.relation.linkage.cardinality.id == 'ONE_TO_ONE(FK)'):
                query = query.filter(or_(
                    getattr(source_type, source_type.get_primary_key_attr_name()) == self.relation_source.id,
                    getattr(source_type, source_type.get_primary_key_attr_name()) == None
                ))
                
            # Group query
            query = query.group_by(target_type.get_primary_key_attr())
        else:
            if query_mode == QueryMode.EXCLUSIVE:
                # Inner join should be sufficient
                if xref_object is None:
                    # The join condition is also explicitely required here for cases with many relations to the same table
                    if self.relation.linkage.cardinality.id == 'ONE_TO_MANY':
                        query = session.query(target_type).join((source_type, source_type.get_primary_key_attr() == getattr(target_type, self.relation.linkage.relation.foreignkeycol)))
                    else:
                        query = session.query(target_type).join((source_type, target_type.get_primary_key_attr() == getattr(source_type, self.relation.linkage.relation.foreignkeycol)))
                else:
                    #n:m, we need to specify the join condition:
                    query = session.query(target_type).join((xref_object, target_type.id == getattr(xref_object, self.relation.linkage.relation.foreignkeycol2)))
                    query = query.join((source_type, and_(source_type.id == getattr(xref_object, self.relation.linkage.relation.foreignkeycol),
                                                        source_type.id == self.relation_source.get_primary_key_attr())
                                      ))
            elif query_mode == QueryMode.WITH_UNLINKED:
                # we require a full outer join
                if xref_object is None:
                    query = session.query(target_type).outerjoin(source_type)
                else:
                    #n:m, we need to specify the join condition:
                    query = session.query(target_type).outerjoin((xref_object, target_type.id == getattr(xref_object, self.relation.linkage.relation.foreignkeycol2)))
                    query = query.join((source_type, or_(and_(source_type.id == getattr(xref_object, self.relation.linkage.relation.foreignkeycol),
                                                        source_type.id == self.relation_source.get_primary_key_attr()),
                                                        source_type.id == None)
                                      ))
            
            if xref_object is None:
                if self.relation.linkage.cardinality.id == 'ONE_TO_MANY':
                    # Foreignkey on target_type side
                    foreignkey_attr = getattr(target_type, self.relation.linkage.relation.foreignkeycol)
                else:
                    # Foreignkey on source_type side
                    foreignkey_attr = getattr(source_type, self.relation.linkage.relation.foreignkeycol)
                   
                query = query.add_column(case([(foreignkey_attr == None, 'false')], else_='true').label('linked')) 
                
                if query_mode == QueryMode.WITH_UNLINKED:
                    query = query.filter(or_(source_type.get_primary_key_attr() == self.relation_source.id, foreignkey_attr == None))
            else:
                # n:m relation
                foreignkeycolumn1 = getattr(xref_object, self.relation.linkage.relation.foreignkeycol)
                foreignkeycolumn2 = getattr(xref_object, self.relation.linkage.relation.foreignkeycol2)
                query = query.add_column(case([(
                    (or_(foreignkeycolumn1 == None,
                    foreignkeycolumn2 == None))
                , 'false')], else_='true').label('linked'))
                
                if query_mode == QueryMode.WITH_UNLINKED:
                    query = query.filter(or_(source_type.get_primary_key_attr() == self.relation_source.id, foreignkeycolumn1 == None, foreignkeycolumn2 == None))
                    
            if query_mode == QueryMode.EXCLUSIVE:
                query = query.filter(getattr(source_type, source_type.get_primary_key_attr_name()) == self.relation_source.id)

        # Check for additional constraints on relation widget
        if hasattr(self.relation, 'filter_clause') and \
                self.relation.filter_clause != None and \
                len(self.relation.filter_clause) > 0:
            query = query.filter(self.relation.filter_clause)
        
        return query


    def query(self, query_mode=None):
        """ Generate an SQL query to obtain the related items of a relation widget's relation through this mixin. """
        assert(self.relation != None)
        assert(self.relation_source != None)
        
        if self.relation.linkage.cardinality.id == 'NONE':
            return self.query_not_joined()
        else:
            return self.query_joined(query_mode)

    def call_subform(self, source_id, setobject_id, linked, alternation):
        """Render subform for a given relation  and setobject."""
        assert(self.relation != None)
        assert(self.relation_source != None)
        session = getUtility(IDbUtility).Session()
        relation = session.query(EmbeddedForm).filter_by(span_identifier=self.relation.id).one()
        plan_identifier = relation.plan_identifier
        if not plan_identifier or len(plan_identifier) == 0:
            raise Exception("plan_identifier is obligatory for relation.")
        
        form_name = relation.form_name
        if not form_name or len(form_name) == 0:
            raise Exception("form_name is obligatory for relation.")

        form = None
        util = getUtility(ILocationProvider)
        genericset = util.get_genericset(plan_identifier)
        if genericset is not None:
            try:
                form = genericset.plan.forms[form_name]
            except AttributeError:
                pass
        if not form:
            return "Requested form unavailable."
        form_view = None
        try:
            if self.request.form['changeableform'] == True:                
                form_view = getMultiAdapter((form, self.request), name='changeableform')
        except KeyError:
            if form_view == None:
                form_view = getMultiAdapter((form, self.request), name='baseform')
        self.request.form['setobject_id'] = setobject_id
        self.request.form['mode'] = 'OPERATIONAL'
        self.request.form['source_id'] = source_id
        self.request.form['linked'] = linked
        self.request.form['show_strip'] = self.show_strip and 'true' or 'false'
        if alternation != None:
            self.request.form['alternation'] = alternation
        else:
            try:
                del(self.request.form['alternation'])
            except KeyError:
                pass
        return form_view()
