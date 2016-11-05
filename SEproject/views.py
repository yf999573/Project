# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse,Http404
from django.shortcuts import render_to_response
from SEproject.models import people
from django.shortcuts import render
from django.template import Context
import datetime
# Create your views here.

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


def register(request):
    errors = []
    account = None
    password = None
    password2 = None
    email = None
    CompareFlag = False

    if request.method == 'POST':
        if not request.POST.get('account'):
            errors.append('Please Enter account')
        else:
            account = request.POST.get('account')
        if not request.POST.get('password'):
            errors.append('Please Enter password')
        else:
            password = request.POST.get('password')
        if not request.POST.get('password2'):
            errors.append('Please Enter password2')
        else:
            password2 = request.POST.get('password2')
        if not request.POST.get('email'):
            errors.append('Please Enter email')
        else:
            email = request.POST.get('email')

        if password is not None and password2 is not None:
            if password == password2:
                CompareFlag = True
            else:
                errors.append('password2 is diff password ')

        if account is not None and password is not None and password2 is not None and email is not None and CompareFlag:
            user = User.objects.create_user(account, email, password)
            user.is_active = True
            user.save
            return HttpResponseRedirect('/account/login')

    return render_to_response('account/register.html', {'errors': errors})


def alogout(request):
    logout(request)
    return HttpResponseRedirect('/index')

def list(requset):
    people_list = people.objects.all()
    c = Context({'people_list':people_list,})
    return render_to_response('list.html',c)

