# -*- coding: utf-8 -*-

import martian
import warnings
import dolmen.content
import grokcore.security
import grokcore.component
from martian.util import scan_for_classes
from zope.component import provideUtility
from zope.interface import verify

from p2.datashackle.management.interfaces import IDatashackleContentFactory


class ContentTypeGrokker(dolmen.content.meta.ContentTypeGrokker):

    def execute(self, content, config, name, factory, require, **kw):

        if not isinstance(name, unicode):
            try:
                name = unicode(name)
            except:
                raise martian.error.GrokError(
                    "%r is not a unicode value. Content `name`"
                    " should be a unicode string." % name)

        content.__content_type__ = name

        if dolmen.content.nofactory.bind().get(content):
            if factory:
                warnings.warn(
                    ("Your Content type has an explicit Factory '%s'."
                     " At the same time you specified the *nofactory*"
                     " directive for your Content type '%s'. The"
                     " factory will be ignored.") %
                     (factory.__name__, content.__name__), UserWarning, 2)
            return True

        elif factory is None:
            utility = dolmen.content.Factory(content)
            verify.verifyObject(dolmen.content.IFactory, utility, tentative=0)
            factory_name = '%s.%s' % (content.__module__, content.__name__)

        else:
            factory_name = grokcore.component.name.bind().get(factory)
            if not factory_name:
                raise martian.error.GrokError(
                    "%r is used as a contenttype factory by %r. "
                    "However, the factory name was omitted. Please, "
                    "use the `name` directive to define a factory name."
                    % (factory, content), factory)
            utility = factory(content)
        
        config.action(
            discriminator=('utility', IDatashackleContentFactory, factory_name),
            callable=provideUtility,
            args=(utility, IDatashackleContentFactory, factory_name),
            )

        return True
