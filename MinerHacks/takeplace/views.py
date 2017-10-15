# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
# from takeplace.models import Event
import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client['newsdata']
collection = db["event_tab"]

events = []

def index(request):

    for item in collection.find():
        events.append(item)

    # page = request.GET.get('ex1', 1)
    # print(request)
    # print(request.GET)

    context = {'events': events[0:3]}

    # context = {
    #     'id': event['id'],
    #     'title': event['title'],
    #     'summary': event['summary'],
    #     'eventDate': event['eventDate'],
    #     'country': event['country'],
    #     'city': event['city']
    # }

    return render(request, 'takeplace/index.html', context)
    # return render(request, 'static/main.html', context)

def contact(request):

    return render(request, 'takeplace/contact.html')
