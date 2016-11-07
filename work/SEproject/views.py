# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import render_to_response
from SEproject.models import SpiderMain
from django.http import HttpResponse
from SEproject import models
from django.template import Context
from SEproject.models import  testhtml

# Create your views here.

def welcome(requset):
    if requset.method == "POST":
        URL = requset.POST.get("URL",None)
        obj_spider = SpiderMain()
        obj_spider.craw(URL)
        print URL
    return render_to_response('welcome.html')

def show(request):
    tstH_list = models.testhtml.objects.all()
    c = Context({"tstH_list":tstH_list})
    return render_to_response('show.html',c)