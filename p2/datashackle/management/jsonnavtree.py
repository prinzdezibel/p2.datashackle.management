# -*- coding: utf-8 -*-
# Copyright (C) projekt-und-partner.de, 2011
# Author: Michael Jenny

import grok

from dolmen.content.interfaces import IContainer
from menhir.simple.navtree.base import JSONNavtreeQuery

from p2.container.interfaces import IParticipationAwareContainer


class JSONNavtreeQuery(JSONNavtreeQuery):
    grok.context(IContainer)

    def _buildTree(self, node):
        node = IParticipationAwareContainer(node, node)
        return super(JSONNavtreeQuery, self)._buildTree(node)
