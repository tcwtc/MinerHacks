# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from mongoengine import *
# from mongoengine import connect
# connect('newsdata', host='127.0.0.1', port=27017)

from django.db import models

# Create your models here.
class Article(models.Model):
    # title = StringField()
    # body = StringField()
    # url = StringField()
    # date = DataTimeField()
    # location = StringField()

    title = models.CharField(max_length=30)
    body = models.CharField(max_length=30)
    url = models.CharField(max_length=30)
    date = models.DateField()
    location = models.CharField(max_length=30)
