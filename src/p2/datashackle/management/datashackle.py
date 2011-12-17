# -*- coding: utf-8 -*-

import dolmen.content as content
import grok
import transaction
from grok.util import create_application
from dolmen.app import security
from zope.app.appsetup.bootstrap import getInformationFromEvent
from zope.app.appsetup.interfaces import IDatabaseOpenedWithRootEvent
from zope.app.appsetup.product import getProductConfiguration
from zope.component import getUtility
from zope.app.wsgi.interfaces import WSGIPublisherApplicationCreated
from zope.site.hooks import setSite
from zope.principalannotation.utility import PrincipalAnnotationUtility
from zope.principalannotation.interfaces import IPrincipalAnnotationUtility
from zope.securitypolicy.interfaces import IRolePermissionManager

from p2.datashackle.core import setup
from p2.datashackle.management.folder import PrivateFolder, Folder
from p2.datashackle.management.generic_set import GenericSet
from p2.datashackle.management.users import Users
from p2.container.container import ignore_enumeration
from p2.datashackle.management import MF as _
from p2.datashackle.management.interfaces import IDatashackle
from p2.datashackle.core.interfaces import IDbUtility


class Datashackle(grok.Application, content.OrderedContainer):
    """The datashackle site manager.
    """
    grok.implements(IDatashackle)
    content.nofactory()
    #grok.local_utility(PAU,
    #                   IAuthentication,
    #                   setup=initialize_pau,
    #                   public=True,
    #                   name_in_container=u"users"
    #                   )


    grok.local_utility(PrincipalAnnotationUtility,
                       IPrincipalAnnotationUtility,
                        public=False
                      )

    title = u"A Datashackle application."


@grok.subscribe(WSGIPublisherApplicationCreated)
def wsgi_app_created(event):
   """Preinstalls the datashackle management application when the zope instance is instantiated."""
   db = event.application.requestFactory._db
   connection = db.open()
   root = connection.root()
   application = root['Application']
   if 'datashackle' not in application:
        name = 'datashackle'
        new_app = create_application(Datashackle, root['Application'], name)
        transaction.commit()
   connection.close()
    
   config = getProductConfiguration('setmanager')
   settings = {
        'provider': config.get('db_provider'),
        'host': config.get('db_host'),
        'user': config.get('db_user'),
        'password': config.get('db_password'),
        'db': config.get('db_name')}
   setup(settings)

@grok.subscribe(IDatabaseOpenedWithRootEvent)
def init_all_applications(event):
    db, connection, root, root_folder = getInformationFromEvent(event)
    for (app_name, app) in root_folder.items():
        setSite(app)

            

@grok.subscribe(grok.IApplicationInitializedEvent)
def init_application(event):
    application = event.object
    if not IDatashackle.providedBy(application):
        # no datashackle grok application
        return          
 
    # Site needs to be setted manually at this point.
    # Otherwise the framework does not notify the catalog to index the newly
    # created propertyform
    setSite(application)
        
    configfolder = PrivateFolder()
    configfolder.title = _(u'Configuration')
    application['configuration'] = configfolder
    # Deny view, edit permission to role dolmen.Owner (which is the default role for our restricted users).
    role_permission = IRolePermissionManager(configfolder)
    role_permission.denyPermissionToRole('dolmen.content.View', 'dolmen.Owner')
    #role_permission.grantPermissionToRole('dolmen.content.View', 'zope.Manager')
    role_permission.denyPermissionToRole('dolmen.content.Edit', 'dolmen.Owner')
    #role_permission.grantPermissionToRole('dolmen.content.Edit', 'zope.Manager')



    metaconfig = PrivateFolder()
    metaconfig.title = _(u'Meta configuration')
    configfolder['meta'] = metaconfig
    ignore_enumeration(metaconfig, 'zope.Everybody') 
 
    users = Users()
    users.title = _(u'Users')
    configfolder['users'] = users
    
    set_ = GenericSet()
    set_.title = u'p2_plan'
    set_.plan_identifier = 'p2_plan'
    set_.table_identifier = 'p2_plan'
    set_.table_key_field = 'plan_identifier'
    metaconfig['p2_plan'] = set_

    set_ = GenericSet()
    set_.title = u'p2_form'
    set_.plan_identifier = 'p2_form'
    set_.table_identifier = 'p2_form'
    set_.table_key_field = 'form_identifier'
    metaconfig['p2_form'] = set_
 
    archetypes = GenericSet()
    archetypes.title = _(u'p2_archetype')
    archetypes.plan_identifier = 'p2_archetype'
    archetypes.table_identifier = 'p2_archetype'
    archetypes.table_key_field = 'id'
    metaconfig['p2_archetypes'] = archetypes
    
    linkageforms = GenericSet()
    linkageforms.title = u'p2_linkage'
    linkageforms.plan_identifier = 'p2_linkage'
    linkageforms.table_identifier = 'p2_linkage'
    linkageforms.table_key_field = 'id'
    metaconfig['p2_linkage'] = linkageforms
    
    set_ = GenericSet()
    set_.title = u'p2_relation'
    set_.plan_identifier = 'p2_relation'
    set_.table_identifier = 'p2_relation'
    set_.table_key_field = 'id'
    metaconfig['p2_relation'] = set_

    widget = GenericSet()
    widget.title = u'p2_widget'
    widget.plan_identifier = 'p2_widget'
    widget.table_identifier = 'p2_widget'
    widget.table_key_field = 'widget_identifier'
    metaconfig['p2_widget'] = widget
    
    set_ = GenericSet()
    set_.title = u'p2_span'
    set_.plan_identifier = 'p2_span'
    set_.table_identifier = 'p2_span'
    set_.table_key_field = 'span_identifier'
    metaconfig['p2_span'] = set_
    
    set_ = GenericSet()
    set_.title = u'p2_span_embeddedform'
    set_.plan_identifier = 'p2_span_embeddedform'
    set_.table_identifier = 'p2_span_embeddedform'
    set_.table_key_field = 'span_identifier'
    metaconfig['p2_span_embeddedform'] = set_
    
    set_ = GenericSet()
    set_.title = u'p2_span_fileupload'
    set_.plan_identifier = 'p2_span_fileupload'
    set_.table_identifier = 'p2_span_fileupload'
    set_.table_key_field = 'span_identifier'
    metaconfig['p2_span_fileupload'] = set_
    
    set_ = GenericSet()
    set_.title = u'p2_span_alphanumeric'
    set_.plan_identifier = 'p2_span_alphanumeric'
    set_.table_identifier = 'p2_span_alphanumeric'
    set_.table_key_field = 'span_identifier'
    metaconfig['p2_span_alphanumeric'] = set_
    
    set_ = GenericSet()
    set_.title = u'p2_span_checkbox'
    set_.plan_identifier = 'p2_span_checkbox'
    set_.table_identifier = 'p2_span_checkbox'
    set_.table_key_field = 'span_identifier'
    metaconfig['p2_span_checkbox'] = set_
    
    set_ = GenericSet()
    set_.title = u'p2_span_dropdown'
    set_.plan_identifier = 'p2_span_dropdown'
    set_.table_identifier = 'p2_span_dropdown'
    set_.table_key_field = 'span_identifier'
    metaconfig['p2_span_dropdown'] = set_
    
    set_ = GenericSet()
    set_.title = u'p2_countries'
    set_.plan_identifier = 'p2_countries'
    set_.table_identifier = 'p2_country'
    set_.table_key_field = 'id'
    metaconfig['p2_span_countries'] = set_

    set_ = GenericSet()
    set_.title = u'Test'
    set_.plan_identifier = 'test'
    set_.table_identifier = 'test'
    set_.table_key_field = 'id'
    application['test'] = set_                     

