# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mongoengine import *
from mongoengine import connect
connect('newsdata', host='127.0.0.1', port=27017)

from django.db import models

# Create your models here.
class Event(Document):
        id = StringField()
        title = StringField()
        summary = StringField()
        eventDate = StringField()
        country = StringField()
        city = StringField()
        lat = FloatField()
        lng = FloatField()
