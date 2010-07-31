# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.utils import simplejson as json
from django.shortcuts import get_object_or_404

from freunde.people.models import *

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
    person = get_object_or_404(Person, pk=guid)
    entry = { 'id'         : person.id,
              'nickname'   : person.nickname,
              'displayName': person.nickname,
              }

    data = { "entry"       : entry,
             "startIndex"  : 0,
             "totalResults": 1,
             }
    content = json.dumps(data, indent=2)
    return HttpResponse(content, content_type=CONTENT_TYPE)

def people_friends(req, guid):
    person = get_object_or_404(Person, pk=guid)

    total = person.friends.count()
    per_page = 50

    entry = []
    for friend in person.friends.all():
        entry.append({ 'id'         : friend.id,
                       'nickname'   : friend.nickname,
                       'displayName': friend.nickname,
                       })

    data = { "entry"        : entry,
             "startIndex"   : 0,
             "itemPerPage"  : per_page,
             "totalResults" : total,
             }
    content = json.dumps(data, indent=2)
    return HttpResponse(content, content_type=CONTENT_TYPE)
