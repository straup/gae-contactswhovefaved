from FlickrApp.Handlers import FlickrAppRequest
from config import config

import cwf.Settings

class Request (FlickrAppRequest) :
    def __init__ (self) :
        FlickrAppRequest.__init__(self, config)

    def check_logged_in (self, min_perms) :

        if not FlickrAppRequest.check_logged_in(self, min_perms) :
            return False

        settings = cwf.Settings.get_settings_for_user(self.user.nsid)
        self.user.settings = settings

        return True
