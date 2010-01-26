from google.appengine.ext import db
from google.appengine.api import memcache

from cwf.Tables import dbSettings
import time

import logging
logging.basicConfig(level=logging.INFO)

def get_settings_for_user (user_nsid, auto_create=True) :

    memkey = "settings_%s" % user_nsid
    cache = memcache.get(memkey)

    if cache is not None :
        return cache

    gql = "SELECT * FROM dbSettings WHERE user_nsid = :1"
    res = db.GqlQuery(gql, user_nsid.strip())

    settings = res.get()

    if not settings and auto_create :
        settings = create_settings_for_user(user_nsid)

    memcache.set(memkey, settings, 3600)
    return settings

def create_settings_for_user (user_nsid) :

    settings = dbSettings()
    settings.user_nsid = user_nsid.strip()
    settings.search_in_contacts_filter = 'all'

    settings.put()

def search_in_contacts_filter (user_nsid, context='all') :

    settings = get_settings_for_user(user_nsid)
    settings.search_in_contacts_filter = context

    __put_settings(user_nsid, settings)

def __put_settings (user_nsid, settings) :
    settings.put()

    memkey = "settings_%s" % user_nsid
    memcache.delete(memkey)
    return settings
