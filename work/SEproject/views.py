# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render_to_response
from SEproject.models import SpiderMain
from SEproject import models
from django.template import Context
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render
from bs4 import BeautifulSoup
import csv
from SEproject.models import  userdata,user
from django.template import RequestContext
# Create your views here.
#用户注册管理
def regist(request):
    if request.method == "POST":
        errors = []
        username = request.POST['username']
        filterResult = models.user.objects.filter(username = username)
        if len(filterResult)>0:
            return HttpResponse("该用户名已注册！")
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
            response =  ["用户名或密码错误，请重新输入！"]
            response =  HttpResponseRedirect('/login/')
            return response
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

# 用户登出管理
def logout(request):
    del request.session['username']
    return HttpResponseRedirect('/login/')

#主页操作判断
def operate(request):
    try:
        URL = request.POST['URL']
        SearchFlag = True
    except:
        SearchFlag = False
    if SearchFlag:
        return search(request)
    else:
        return welcome(request)

#进入主页
def welcome(request):
    username = request.session["username"]
    return render_to_response('mainview.html',{'username':username})

#URL爬取管理
def search(request):
    if request.method == "POST":
        user_name = request.session["username"]
        URL = request.POST["URL"]
        if len(URL) == 0:
            return HttpResponseRedirect("/welcome/")
        else:
            obj_spider = SpiderMain()
            nov_times = obj_spider.craw(URL,user_name)
            if (nov_times == None):
                return HttpResponse("输入URL地址有误！")
            else:
                data = models.userdata.objects.filter(name=user_name, time=nov_times)
                if len(data)>0:
                    datas = Context({"nov_data": data})
                    return render_to_response('show.html', datas)
                else:
                    return HttpResponse("该网页无格式化数据！")
    else:
        return render_to_response('mainview.html')

#历史纪录查询
def hislist(request):
    user_name = request.session["username"]
    cont = models.userdata.objects.filter(name = user_name).count()
    if(cont == False):
        return render(request,'Dishis_show.html')
    else:
        his_list = models.userdata.objects.filter(name = user_name)
        datas = Context({"his_list":his_list})
        return render_to_response('his_show.html',datas)
#导出文件
def some_view(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="datas.csv"'
    writer = csv.writer(response)
    user_name = request.session["username"]
    table_data = models.userdata.objects.filter(name = user_name)
    for item in table_data:
        soup_all = BeautifulSoup(item.date)
        tr_nov = soup_all.find_all('tr')
        for tr in tr_nov:
            br_tds = tr.find_all(['th', 'td'])
            tds = [td.get_text().encode('gbk') for td in br_tds]
            writer.writerow(tds)
        writer.writerow([])
    return response