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
from reportlab.pdfgen import canvas
import pdfcrowd
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
            error = "该用户名已注册！"
            errors = Context({"errors": error})
            return render_to_response('erroe.html', errors)
        else:
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            email = request.POST['email']
            if not email:
                error = "验证邮箱不可为空！"
                errors = Context({"errors":error})
                return render_to_response("erroe.html",errors)
            else:
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
        old_user = models.user.objects.filter(username = username)
        if old_user:
            old_user_pwd=models.user.objects.filter(username=username,password=password)
            if old_user_pwd:
                response =  HttpResponseRedirect('/welcome/')
                request.session['username'] = username
                return response
            else:
                error = "密码错误，请重新输入！"
                errors = Context({"errors": error})
                return render_to_response('erroe.html', errors)
        else:
            error =  "用户不存在，请重新输入！"
            errors = Context({"errors": error})
            return render_to_response('erroe.html',errors)
    else:
        return render_to_response("login.html")

#用户密码找回
def changepwd(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        exist_user = models.user.objects.filter(username=username)
        if exist_user:
            exist__mail = models.user.objects.filter(username=username,email=email)
            if exist__mail:
                exist__mail.update(password = password)
                response = HttpResponseRedirect('/user/')
                return response
            else:
                error = "验证邮箱信息错误！"
                errors = Context({"errors": error})
                return render_to_response('erroe.html', errors)
        else:
            error = "用户名不存在！"
            errors = Context({"errors": error})
            return render_to_response('erroe.html', errors)
    else:
        response = HttpResponseRedirect('/user/')
        return response

def test(request):
    return render_to_response("change.html");

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
    return HttpResponseRedirect('/user/')

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
                error = "输入URL地址有误！"
                errors = Context({"errors": error})
                return  render_to_response('show_error.html',errors)
            else:
                data = models.userdata.objects.filter(name=user_name, time=nov_times)
                if data.count() > 0:
                    table_list = []
                    for item in data:
                        soup = BeautifulSoup(item.date)
                        tr_node = soup.find_all('tr')
                        tr_list = []
                        for tr in tr_node:
                            hd_data = tr.find_all(['th', 'td'])
                            hds = [hd.get_text() for hd in hd_data]
                            tr_list.append(hds)
                        table_list.append(tr_list)
                    data_set = Context({"table_list": table_list})
                    return render_to_response('show.html', data_set)
                else:
                    error = "该网页无格式化数据！"
                    errors = Context({"errors": error})
                    return render_to_response('show_error.html', errors)
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
def outfile(request):
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
            tds = [td.get_text().encode('gb18030') for td in br_tds]
            writer.writerow(tds)
        writer.writerow([])
    return response