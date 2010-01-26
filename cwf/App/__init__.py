from config import config

import cwf
import cwf.Settings

import time
import logging
import md5

class CwfException (Exception) :

  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)

class CwfAPIException (CwfException) :

  def __init__(self, value):
    self.value = value

class Main (cwf.Request) :

  def get (self):

    if not self.check_logged_in(self.min_perms) :
        self.display("main_logged_out.html")
        return

    refresh = 1800
    now = int(time.time())
    dt = now - refresh

    self.assign('min_fave_date', dt)
    self.assign('refresh', refresh)

    contacts_crumb = self.generate_crumb(self.user, 'method=contacts')
    self.assign('contacts_crumb', contacts_crumb)

    self.display("main_logged_in.html")
    return

class Settings (cwf.Request) :

    def get (self) :

        if not self.check_logged_in(self.min_perms) :
            self.do_flickr_auth(self.min_perms)
            return

        settings_crumb = self.generate_crumb(self.user, 'method=settings')
        self.assign('settings_crumb', settings_crumb)

        self.display('settings.html')
        return

    def post (self) :

        if not self.check_logged_in(self.min_perms) :
            self.do_flickr_auth(self.min_perms)
            return

        if not self.validate_crumb(self.user, 'method=settings', self.request.get('crumb')) :
            self.assign('error', 'invalid_crumb')
            self.display('settings.html')
            return

        filter = self.request.get('filter')

        if not filter in ('all', 'ff') :
            self.assign('error', 'invalid_filter')
            self.display('settings.html')
            return

        cwf.Settings.search_in_contacts_filter(self.user.nsid, filter)
        self.redirect('/')
