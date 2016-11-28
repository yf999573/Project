# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse,Http404
from django.shortcuts import render_to_response
from SEproject.models import people
from django.shortcuts import render
from django.template import Context
import datetime
# Create your views here.
#用户注册管理
def regist(request):
    if request.method == "POST":
        errors = []
        username = request.POST['username']
        filterResult = models.user.objects.filter(username = username)
        if len(filterResult)>0:
            error = "该用户名已注册！"
            errors = Context({"errors": error})
            return render_to_response('erroe.html', errors)
        else:
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            email = request.POST['email']
            new_user = models.user.objects.create(username=username, password=password2,email=email)
            new_user.save()
            response = HttpResponseRedirect('/welcome/')
            request.session['username'] = username
            return response
    else:
        return render_to_response('login.html')
#用户登录管理
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        old_user = models.user.objects.filter(username = username,password = password)
        if old_user:
            response =  HttpResponseRedirect('/welcome/')
            request.session['username'] = username
            return response
        else:
            error =  "用户名或密码错误，请重新输入！"
            errors = Context({"errors": error})
            return render_to_response('erroe.html',errors)
    else:
        return render_to_response("login.html")
#用户管理行为判断
def loginR(request):
    try:
        password1 = request.POST['password1']
        loginFlag = False
    except:
        loginFlag = True
    if loginFlag:
        return login(request)
    else:
        return regist(request)

# 找回密码
def findback():
    return 0


# 用户登出管理
def logout(request):
    del request.session['username']
    return HttpResponseRedirect('/login/')

def alogin(request):
    errors = []
    account = None
    password = None
    if request.method == 'POST':
        if not request.POST.get('account'):
            errors.append('Please Enter account')
        else:
            account = request.POST.get('account')
        if not request.POST.get('password'):
            errors.append('Please Enter password')
        else:
            password = request.POST.get('password')
        if account is not None and password is not None:
            user = authenticate(username=account, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/index')
                else:
                    errors.append('disabled account')
            else:
                errors.append('invaild user')
    return render_to_response('account/login.html', {'errors': errors})


def alogout(request):
    logout(request)
    return HttpResponseRedirect('/index')

def list(requset):
    people_list = people.objects.all()
    c = Context({'people_list':people_list,})
    return render_to_response('list.html',c)

