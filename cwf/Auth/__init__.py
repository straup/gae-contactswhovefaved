import cwf
import FlickrApp

class TokenDance (cwf.Request) :

  def get (self):

    try :

      self.do_token_dance()

    except FlickrApp.FlickrAppAPIException, e :

      self.assign('error', 'api_error')

    except FlickrApp.FlickrAppException, e :

      self.assign('error', 'app_error')
      self.assign('error_message', e)

    except Exception, e:

      self.assign('error', 'unknown')
      self.assign('error_message', e)

    self.display("token_dance.html")
    return

class Signin (cwf.Request) :

    def get (self) :
        if self.check_logged_in(self.min_perms) :
            self.redirect("/")

        self.do_flickr_auth(self.min_perms, '/')
        return

class Signout (cwf.Request) :

    def get (self) :

        if not self.check_logged_in(self.min_perms) :
            self.redirect("/")

        logout_crumb = self.generate_crumb(self.user, 'method=logout')
        self.assign('logout_crumb', logout_crumb)

        self.display("signout.html")
        return

    def post (self) :

        if not self.check_logged_in(self.min_perms) :
            self.redirect("/")

        crumb = self.request.get('crumb')

        if not crumb :
            self.redirect("/")

        if not self.validate_crumb(self.user, "logout", crumb) :
            self.redirect("/")

        self.response.headers.add_header('Set-Cookie', 'ffo=')
        self.response.headers.add_header('Set-Cookie', 'fft=')

        self.redirect("/")
