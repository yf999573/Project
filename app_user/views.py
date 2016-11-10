# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from app_user import models
from django.shortcuts import render_to_response
from django.template import Context
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponse
from django import forms

from django.template import RequestContext
from models import message
# Create your views here.

class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=20)
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput())
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput())
    email = forms.EmailField(label='电子邮件')

class UserFormLogin(forms.Form):
    username = forms.CharField(label='用户名', max_length=20)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())

#注册
def regist(request):
    if request.method == "POST":
        uf = UserForm(request.POST)
        errors = []
        if uf.is_valid():
            username = uf.cleaned_data['username']
            #print username
            filterResult = models.message.objects.filter(username = username)
            if filterResult:
                errors.append("用户名已存在！")
                return render_to_response('regist.html',{'errors':errors})
            else:
                password1 = uf.cleaned_data['password1']
                password2 = uf.cleaned_data['password2']
                if (password2 != password1):
                    errors.append("两次输入的密码不一致！")
                    return render_to_response('regist.html',{'errors':errors})
                password = password2
                email = uf.cleaned_data['email']
                new_user = models.message.objects.create(username=username, password=password1,email=email)
                new_user.save()
                #return render_to_response('regist.html')
                return HttpResponseRedirect('/login/')
    else:
        uf = UserForm()
    return render_to_response('regist.html',{'uf':uf})

#登录

def login(request):
    if request.method == "POST":
        uf = UserFormLogin(request.POST)
        if uf.is_valid():
            username_ex = uf.cleaned_data['username']
            password_ex = uf.cleaned_data['password']
            old_user = models.message.objects.filter(username = username_ex,password = password_ex)
            print username_ex,password_ex
            if old_user:
                response =  HttpResponseRedirect('/welcome/')
                request.session['username'] = username_ex
                return response
            else:
                return HttpResponseRedirect('/login/')
    else:
        uf = UserFormLogin()
    return render_to_response("login.html",{'uf':uf})

def welcome(req):
    username = req.session["username"]
    return render_to_response('mainview.html',{'username':username})
#登出
def logout(request):
    del request.session['username']
    return HttpResponse('logout ok!')