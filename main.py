#!/usr/bin/env python

import wsgiref.handlers
from google.appengine.ext import webapp

import cwf.App
import cwf.Auth
import cwf.API

if __name__ == '__main__':

  handlers = [
    ('/', cwf.App.Main),
    ('/settings', cwf.App.Settings),
    ('/signout', cwf.Auth.Signout),
    ('/signin', cwf.Auth.Signin),
    ('/auth', cwf.Auth.TokenDance),
    ('/api', cwf.API.Dispatch),    ]

  application = webapp.WSGIApplication(handlers, debug=False)
  wsgiref.handlers.CGIHandler().run(application)
