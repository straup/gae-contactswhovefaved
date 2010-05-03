from FlickrApp.API import FlickrAppAPI
import cwf
import time
import md5
from config import config

class Dispatch (cwf.Request, FlickrAppAPI) :

    def __init__ (self):

	cwf.Request.__init__(self)
	FlickrAppAPI.__init__(self)

	self.set_handler('POST', 'contacts', 'api_get_contacts')
	self.set_handler('POST', 'faves', 'api_get_faves')

    def api_get_contacts (self) :

	if not self.check_logged_in(self.min_perms) :
	    self.api_error(403)
	    return

	required = ('crumb',)

	if not self.ensure_args(required) :
	    return

	if not self.ensure_crumb('method=contacts') :
	    return

        self.check_useragent()

        if self.browser['mobile']:
            config['cwf_offset_hours'] = config['cwf_offset_hours'] / 2

	refresh = 1800 * config['cwf_offset_hours']
	now = int(time.time())

	dt = now - refresh

	try :
	    method = 'flickr.contacts.getListRecentlyFaved'

	    args = {
		'auth_token' : self.user.token,
		'filter' : self.user.settings.search_in_contacts_filter,
		'date_lastfaved' : dt,
		}

	    rsp = self.api_call(method, args)

	except Exception, e :

	    self.api_error(1999, 'Failed to get any contacts: %s' % e)
	    return

	"""
	if rsp['contacts']['total'] == 0:
	    rsp['contacts']['contact'].append({
		'nsid' : '35034348999@N01',
		'username' : 'straup',
		})

	    rsp['contacts']['total'] = 1
	"""

	for c in rsp['contacts']['contact'] :

	    nsid = c['nsid']
	    icon = self.flickr_get_buddyicon(nsid)

	    c['buddyicon'] = icon
	    c['hex'] = md5.new(nsid).hexdigest()
	    c['short_hex'] = c['hex'][0:6]

	rsp = { 'contacts' : rsp['contacts'] }
	return self.api_ok(rsp)

    def api_get_faves(self):

	if not self.check_logged_in(self.min_perms) :
	    self.api_error(403)
	    return

	required = ('crumb', 'user_id')

	if not self.ensure_args(required) :
	    return

	if not self.ensure_crumb('method=contacts') :
	    return

	refresh = 1800 * config['cwf_offset_hours']
	now = int(time.time())
	dt = now - refresh

	user_id = self.request.get('user_id')

	try :

	    method = 'flickr.favorites.getList'

	    args = {
		'auth_token' : self.user.token,
		'user_id' : user_id,
		'min_fave_date' : dt,
		'extras' : 'owner_name,o_dims,url_sq,url_t,url_s,url_m',
		}

	    rsp = self.api_call(method, args)

	except Exception, e:
	    self.api_error(999, 'Failed to get any photos for %s: %s' % (nsid, e));
	    return

	rsp = { 'photos' : rsp['photos'] }
	return self.api_ok(rsp)
