# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns(
    'freunde.people.views',

    (r'@me/@self$', 'people_me_self'),
    (r'@me/@friends$', 'people_me_friends'),
    (r'@me/@all$', 'people_me_friends'),

    (r'(?P<guid>[^/]+)/@self$', 'people_self'),
    (r'(?P<guid>[^/]+)/@friends$', 'people_friends'),
    (r'(?P<guid>[^/]+)/@all$', 'people_friends'),

    #(r'(?P<guid>[^/]+)/@friends/(?P<friend_guid>[^/]+)', ''),
)
