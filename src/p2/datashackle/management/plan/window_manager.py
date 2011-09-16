# -*- coding: utf-8 -*-
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# A copy of the GNU General Public License is included in the
# documentation.
#
# Copyright (C) projekt-und-partner.com, 2010
#
# Author:  Michael Jenny <michael.jenny%40projekt-und-partner.com>

import grok
from zope.interface import Interface

from p2.datashackle.core.interfaces import IGenericSet
from p2.windowmanager.layout import WindowManager


class WindowManagerVM(grok.ViewletManager):
    grok.name("windowmanager")
    grok.context(Interface)


class WindowManager(WindowManager):
    grok.context(IGenericSet)
    grok.viewletmanager(WindowManagerVM)
    grok.order(20)
