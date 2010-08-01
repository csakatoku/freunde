# -*- coding: utf-8 -*-
import cgi
import urllib
import functools

import oauth2 as oauth

from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.utils import simplejson as json
from django.shortcuts import get_object_or_404

from freunde.people.models import *

CONTENT_TYPE = 'text/json'

class OAuthRequest(oauth.Request):
    @staticmethod
    def _split_url_string(param_str):
        """Turn URL string into parameters."""
        parameters = cgi.parse_qs(param_str, keep_blank_values=True)
        for k, v in parameters.iteritems():
            parameters[k] = urllib.unquote(v[0])
        return parameters

def oauth_required(func):
    server = oauth.Server()
    server.add_signature_method(oauth.SignatureMethod_PLAINTEXT())
    server.add_signature_method(oauth.SignatureMethod_HMAC_SHA1())

    def inner(req, *args, **kwds):
        if req.is_secure():
            http_url = 'https://%s%s' % (req.get_host(), req.path)
        else:
            http_url = 'http://%s%s' % (req.get_host(), req.path)

        headers = { 'Authorization': req.META.get('HTTP_AUTHORIZATION', '') }
        query_string = req.META.get('QUERY_STRING', '')
        if req.method == 'POST':
            if req.META.get('CONTENT_TYPE', '').startswith('application/x-www-form-urlencoded'):
                if query_string:
                    query_string += '&' + req.raw_post_data
                else:
                    query_string = req.raw_post_data

        oauth_req = OAuthRequest.from_request(
            http_method=req.method,
            http_url=http_url,
            headers=headers,
            query_string=query_string)

        if oauth_req is None:
            return HttpResponseBadRequest('param missing')

        oauth_token = oauth_req.get('oauth_token')
        oauth_token_secret = oauth_req.get('oauth_token_secret')
        if oauth_token and oauth_token_secret:
            token = oauth.Token(oauth_token, oauth_token_secret)
        else:
            token = None

        consumer_key = oauth_req.get('oauth_consumer_key')
        if consumer_key is None:
            return HttpResponseBadRequest()

        app = get_object_or_404(Application, consumer_key=consumer_key)
        oauth_consumer = oauth.Consumer(app.consumer_key, app.consumer_secret)

        try:
            server.verify_request(oauth_req, oauth_consumer, token)
        except Exception, e:
            return HttpResponseBadRequest(str(e))

        req.app = app
        return func(req, *args, **kwds)

    return functools.wraps(func)(inner)

@oauth_required
def people_me_self(req):
    guid = req.GET.get('xoauth_requestor_id')
    if not guid:
        return HttpResponseBadRequest('xoauth_requestor_id required')
    return people_self(req, guid)

@oauth_required
def people_me_friends(req):
    guid = req.GET.get('xoauth_requestor_id')
    if not guid:
        return HttpResponseBadRequest('xoauth_requestor_id required')
    return people_friends(req, guid)

@oauth_required
def people_self(req, guid):
    person = get_object_or_404(Person, pk=guid)
    entry = { 'id'          : person.id,
              'nickname'    : person.nickname,
              'displayName' : person.nickname,
              }

    data = { "entry"       : entry,
             "startIndex"  : 0,
             "totalResults": 1,
             }
    content = json.dumps(data, indent=2)
    return HttpResponse(content, content_type=CONTENT_TYPE)

@oauth_required
def people_friends(req, guid):
    person = get_object_or_404(Person, pk=guid)

    total = person.friends.count()
    per_page = 50

    entry = []
    for friend in person.friends.all():
        entry.append({ 'id'          : friend.id,
                       'nickname'    : friend.nickname,
                       'displayName' : friend.nickname,
                       })

    data = { "entry"        : entry,
             "startIndex"   : 0,
             "itemPerPage"  : per_page,
             "totalResults" : total,
             }
    content = json.dumps(data, indent=2)
    return HttpResponse(content, content_type=CONTENT_TYPE)
