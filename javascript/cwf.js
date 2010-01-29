function show_who (id){
    $("#" + id).css('opacity', 1);
}

function hide_who (id){
    $("#" + id).css('opacity', 0);
}

//

if (! info){
    var info = {};
}

if (! info.aaronland){
    info.aaronland = {};
}

if (! info.aaronland.cwf){
    info.aaronland.cwf = {};
}

info.aaronland.cwf.Photos = function(args){
    this.args = args;

    this.pending_contacts = 0;

    this.contacts = new Object();
    this.faves = new Array();

    this.current_photo = null;
    this.shown = null;

    var api_args = {
        'host' : this.args['host'],
    };

    this.api = new info.aaronland.flickrapp.API(api_args);
};

info.aaronland.cwf.Photos.prototype.get_contacts = function(){

    this.pending_contacts = 0;
    this.contacts = new Object();
    this.faves = new Array();

    var _self = this;

    var doThisOnSuccess = function(rsp){

	var total = rsp['contacts']['total'];

	_self.pending_contacts = total;

	if (total == 0){
	    _self.status('There are no new favorites from your contacts.', 1);
	    return;
	}

	if (total == 1){
	    _self.status("There is 1 contact with new faves! Fetching them now...");
	}

	else {
	    _self.status("There are " + total + " contacts with new faves! Rounding them up now...");
	}

	for (var i=0; i < total; i++){

	    var contact = rsp['contacts']['contact'][i];
	    _self.get_faves_for_contact(contact);
	}

	_self.wait_for_faves();
    };

    var doThisIfNot = function (rsp){

	var msg = 'Ack! There was a problem finding your contacts with new faves.';

	msg += '<div style="margin-top:15px;font-size:small;">';
	msg += 'The robot squirrels report <q>' + rsp['error']['message'] + '.</q> ';
	msg += '<a href="/">Would you like to try again?</a>';
	msg += '</div>';

	_self.status(msg, 1);
	return;
    };

    var args = {
        'crumb' : this.args['contacts_crumb'],
        'format' : 'json',
    }

    this.api.api_call('contacts', args, doThisOnSuccess, doThisIfNot);
};

info.aaronland.cwf.Photos.prototype.get_faves_for_contact = function(contact){

    this.contacts[ contact['nsid'] ] = contact;

    var _self = this;
    var _contact = contact;

    var doThisOnSuccess = function(rsp){

	var total = rsp['photos']['photo'].length;

	if (total == 0){
	    _self.status('Hrmph! Something went wrong gathering new faves from ' + _self.scrub(contact['username'], 1));
	    _self.pending_contacts -= 1;
	    return;
	}

	if (total == 1){
	    _self.status(_self.scrub(contact['username'], 1) + ' has 1 new favourited photo!');
	}

	else {
	    _self.status(_self.scrub(contact['username'], 1) + ' has ' +  total + ' new faves!');
	}

	for (var i=0; i < total; i++){
	    var photo = rsp['photos']['photo'][i];
	    photo['faved_by'] = _contact['nsid'];
	    _self.faves.push(photo);
	}

	_self.pending_contacts -= 1;
	return;
    };

    var doThisIfNot = function (rsp){
	_self.status('Hrmph! Something went wrong gathering new faves from ' + _self.scrub(contact['username'], 1));
	_self.pending_contacts -= 1;
	return;
    };

    var args = {
        'crumb' : this.args['contacts_crumb'],
	'user_id' : contact['nsid'],
        'format' : 'json',
    }

    this.api.api_call('faves', args, doThisOnSuccess, doThisIfNot);
    return;
};

info.aaronland.cwf.Photos.prototype.wait_for_faves = function(){

    var _self = this;

    if (this.pending_contacts == 0){
	this.show_faves();
	return;
    }

    var delay =  Math.floor(Math.random() * 2000);
    this.log("pending contacts: " + this.pending_contacts + " wait: " + delay);

    setTimeout(function(){
	    _self.wait_for_faves();
	}, delay);
};

info.aaronland.cwf.Photos.prototype.show_faves = function(){

    var by_date = new Object;
    var total = this.faves.length;

    for (var i=0; i < total; i++){
	var fave = this.faves[i];
	var df = fave['date_faved'];

	// the chances of two people faving something at
	// the same time are basically nil but just in case...

	while (by_date[ df ]){
	    df -= 1;
	}

	by_date[ df ] = fave;
    }

    var dates = new Array();

    for (ts in by_date){
	dates.push(ts);
    }

    dates.sort().reverse();

    for (var i in dates){
	var df = dates[i];
	var fave = by_date[ df ];
	this.display_fave(fave);
    }

    this.status('');
};

info.aaronland.cwf.Photos.prototype.display_fave = function(fave){

    var photo_page = this.photo_page(fave);
    var photo_thumb = this.photo_url(fave, 's');

    var contact = this.contacts[ fave['faved_by'] ];
    var contact_url = 'http://www.flickr.com/photos/' + contact['nsid'];
    var contact_icon = contact['buddyicon'];

    var hex = contact['hex'];
    var short_hex = contact['short_hex'];

    var target = '_flickr_' + hex;
    var buddyicon_id = 'buddyicon_' + hex + '_' + fave['id'];

    var alt = this.scrub(contact['username'], 1) + ' faved ' + this.scrub(fave['title'], 1) + ', by ' + this.scrub(fave['ownername'], 1);

    // wrapper

    var html = '';
    html += '<div style="float:left; margin-right:20px;margin-bottom:15px;">';

    // buddyicon

    html += '<div style="float:left;background-color:#' + short_hex + ';background-image:url(/images/tran.gif);">';
    html += '<a target="_contact" href="' + contact_url + '/faves">';
    html += '<img src="' + contact_icon + '" height="24" width="24" class="buddyicon" id="' + buddyicon_id + '" />';
    html += '</a>';
    html += '</div>';

    // thumb

    html += '<a href="' + photo_page + '" target="' + target + '" title="' + alt + '">';
    html += '<img src="' + photo_thumb + '" height="75" width="75" style="border:0px solid #' + short_hex + ';" ';
    html += 'onmouseover="show_who(\'' + buddyicon_id + '\');" onmouseout="hide_who(\'' + buddyicon_id + '\');" ';
    html += 'alt="' + alt + '" ';
    html += '/>';
    html += '</a>';

    // date

    // html += '<div style="text-align:right;font-size:11px;margin-top:6px;">';
    // html += 'when';
    // html += '</div>';

    // wrapper

    html += '</div>';
    $("#faves").append(html);
};

info.aaronland.cwf.Photos.prototype.photo_page = function(ph){
    return 'http://www.flickr.com/photos/' + ph['owner'] + '/' + ph['id'];
};

info.aaronland.cwf.Photos.prototype.photo_url = function(ph, sz){
    url = 'http://farm' + ph['farm'] + '.static.flickr.com/' + ph['server'] + '/' + ph['id'] + '_' + ph['secret'];

    if (sz){
	url = url + '_' + sz;
    }

    url = url + '.jpg';
    return url;
};

info.aaronland.cwf.Photos.prototype.status = function(msg, is_error){

    if (msg == ''){
	$("#status").html('');
	return;
    }

    if (is_error){
	msg = '<img src="/images/rainbow.gif" height="100" width="100" align="middle" style="margin-right:40px;float:left;" />' + msg;
    }

    else {
	msg = '<img src="/images/cat.gif" height="92" width="100" align="middle" style="margin-right:40px;float:left;" />' + msg;
    }

    msg += '<br clear="all" />';

    $("#status").html(msg);
    return;
};

info.aaronland.cwf.Photos.prototype.log = function(msg){
    // console.log(msg);
}

info.aaronland.cwf.Photos.prototype.scrub = function(str, allow_whitespace){

    str = str.replace(/^\s+/, '');
    str = str.replace(/\s+$/, '');

    str = encodeURIComponent(str);

    if (allow_whitespace){
        str = str.replace(/%20/g, " ");
    }

    return str;
};