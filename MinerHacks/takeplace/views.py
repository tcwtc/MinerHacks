# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyBNIsqGlDQqLRVQpeVrXTKxtAHgGHjh5lk')

from django.shortcuts import render
from takeplace.models import Event
import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client['newsdata']
collection = db["event_tab"]


def index(request):
    events = []

    if request.method == 'GET':
        context = {'events': events[0:3]}
    elif request.method == 'POST':

        date_selected = request.POST['date']
        date_selected = date_selected[6:10] + '-' + date_selected[0:2] + '-' + date_selected[3:5]

        for item in collection.find({"eventDate": date_selected}):
            event = Event()
            event.id = item['id']
            event.title = item['title']
            event.summary = item['summary']
            event.eventDate = item['eventDate']
            event.country = item['country']
            event.city = item['city']
            # geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
            geocode_result = gmaps.geocode(event.city + ', ' + event.country)
            event.lat = float(geocode_result[0]['geometry']['location']['lat'])
            event.lng = float(geocode_result[0]['geometry']['location']['lng'])
            events.append(event)

        context = {'events': events, 'date': date_selected}

    # if request.method == 'GET':
    #     context = {'events': events[0:3]}
    # elif request.method == 'POST':
    #     context = {'events': events[0:3], 'date': request.POST['date']}

    return render(request, 'takeplace/index.html', context)


from datetime import datetime
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


# Add the following function to the end of myblog/views.py
# def post_upload(request):
#     if request.method == 'GET':
#         return render(request, 'takeplace/upload.html', {})
#     elif request.method == 'POST':
#         post = {'content': request.POST['content']}
#         # No need to call post.save() at this point -- it's already saved.
#         return render(request, 'takeplace/upload.html', post)
