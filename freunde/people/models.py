# -*- coding: utf-8 -*-
from django.db import models

class Application(models.Model):
    name            = models.CharField(max_length=50)
    consumer_key    = models.CharField(max_length=250, unique=True)
    consumer_secret = models.CharField(max_length=250)

    def __unicode__(self):
        return self.name

class Person(models.Model):
    nickname   = models.CharField(max_length=50)
    blood_type = models.CharField(max_length=2)
    address    = models.CharField(max_length=250)
    birthday   = models.DateField()
    gender     = models.CharField(max_length=1)
    user_hash  = models.CharField(max_length=250)
    friends    = models.ManyToManyField('Person')
    apps       = models.ManyToManyField('Application')

    def __unicode__(self):
        return self.nickname

