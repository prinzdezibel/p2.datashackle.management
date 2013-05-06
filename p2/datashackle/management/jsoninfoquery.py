# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.com, 2011
# Author:  Jonas Thiem <jonas.thiem%40projekt-und-partner.com>

import grok
import json
import sqlalchemy
from zope.component import getUtility

from p2.datashackle.core.interfaces import IDbUtility 
from p2.datashackle.management.plan.plan import Plan
from p2.datashackle.management.interfaces import IDatashackle


class JsonInfoQuery(grok.View):
    """ This is the JsonInfoQuery view that sits on the application and
    offers various information to be requested through JS. It uses the
    JsonInfoQuery utility which implements the required logic to gather
    the data in question.
    It is supposed to give you very generic information like the existing
    plans in this application and other things. """
    
    grok.name('jsoninfoquery')
    grok.context(IDatashackle)
    
    def get_plan_table_info(self):
        """ Dump a JSON dictionary which associates all plan identifiers with their respective table identifiers """
        dictionary = {}
        session = getUtility(IDbUtility).Session()
        plans = session.query(Plan).all()
        for plan in plans:
            dictionary[plan.plan_identifier] = plan.table_identifier
        return json.dumps(dictionary)
    
    def render(self):
        self.response.setHeader('Content-Type', 'application/json')
        return self.get_plan_table_info()


