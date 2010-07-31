# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.utils import simplejson as json

CONTENT_TYPE = 'text/json'

def people_me_self(req):
    guid = req.GET.get('xoauth_requestor_id')
    if not guid:
        return HttpResponseBadRequest('xoauth_requestor_id required')
    return people_self(req, guid)

def people_me_friends(req):
    guid = req.GET.get('xoauth_requestor_id')
    if not guid:
        return HttpResponseBadRequest('xoauth_requestor_id required')
    return people_friends(req, guid)

def people_self(req, guid):
    content = json.dumps({})
    return HttpResponse(content, content_type=CONTENT_TYPE)

def people_friends(req, guid):
    content = json.dumps({})
    return HttpResponse(content, content_type=CONTENT_TYPE)


