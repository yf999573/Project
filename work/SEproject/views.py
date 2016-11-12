# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import render_to_response
from SEproject.models import SpiderMain
from django.http import HttpResponse
from SEproject import models
from django.template import Context
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponse
from SEproject.models import  testhtml
from django import forms
from django.template import RequestContext
from models import message

# Create your views here.
def regist(request):
    if request.method == "POST":
        errors = []
        username = request.POST['username']
        filterResult = models.message.objects.filter(username = username)
        if filterResult:
            errors.append("用户名已存在！")
            return render_to_response('login.html',{'errors':errors})
        else:
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if (password2 != password1):
                errors.append("两次输入的密码不一致！")
                return render_to_response('login.html',{'errors':errors})
            password = password2
            email = request.POST['email']
            new_user = models.message.objects.create(username=username, password=password,email=email)
            new_user.save()
            response = HttpResponseRedirect('/welcome/')
            request.session['username'] = username
            return response
    else:
        return render_to_response('login.html')

#登录
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        old_user = models.message.objects.filter(username = username,password = password)
        if old_user:
            response =  HttpResponseRedirect('/welcome/')
            request.session['username'] = username
            return response
        else:
            return HttpResponseRedirect('/login/')
    else:
        return render_to_response("login.html",)

#注册
def welcome(req):
    username = req.session["username"]
    return render_to_response('mainview.html',{'username':username})
#登出
def logout(request):
    del request.session['username']
    return HttpResponseRedirect('/login/')

def loginR(request):
    try:
        password1 = request.POST['password1']
        loginFlag=False
    except:
        loginFlag=True
    if loginFlag:
        return login(request)
    else:
        return regist(request)


def search(requset):
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