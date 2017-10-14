# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from takeplace.models import Article

# Create your views here.
def index(request):
    # limit = 15
    article = Article
    # print(request)
    # print(request.GET)

    context = {
        'title': article.title,
        'body': article.body,
        'url': article.url,
        'date': article.date,
        'location': article.location,
    }

    return render(request, 'takeplace/index.html')
