# -*- coding: utf-8 -*-

import grok

from dolmen.forms.base import ApplicationForm

from zeam.form.base import Fields, action, Action, Actions
from zeam.form.base.markers import SUCCESS, FAILURE
from zeam.form.ztk.actions import CancelAction

from p2.datashackle.management import MF as _
from p2.datashackle.management.interfaces import IUserPreferences


class UserPreferencesFormPage(ApplicationForm):
    grok.name('index')
    grok.context(IUserPreferences)
    grok.require('setmanager.Edit')

    ignoreContent = False
    ignoreRequest = False
    actions = Actions(CancelAction(_("Cancel")),)

    label = _(u"Edit preferences")

    @action(u"Save")
    def handle_save_action(self):
        data, errors = self.extractData()
        if errors:
            self.submissionError = errors
            return FAILURE
        self.context.preferred_lang = data['preferred_lang']
        self.context.preferred_date = data['preferred_date']
        
        self.flash(_(u"Preferences updated"))
        self.redirect(self.url(self.context))

        return SUCCESS

    @property
    def fields(self):
        fields = Fields(IUserPreferences).omit('__parent__', 'title')
        return fields

