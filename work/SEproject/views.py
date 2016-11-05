# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from SEproject.models import SpiderMain
from django.http import HttpResponse

# Create your views here.

def search(request,url_root):
    obj_spider = SpiderMain()
    obj_spider.craw(url_root)
    return HttpResponse('success search')