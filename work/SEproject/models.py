# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import urllib2
from bs4 import BeautifulSoup
import datetime
#用户信息表
class user(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=15)
    email = models.EmailField(default= 'blank@qq.com')

    def __unicode__(self):
        return self.username
#用户数据表
class userdata(models.Model):
    name = models.CharField(max_length=20)
    url = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    time = models.DateTimeField()
    date = models.TextField()
#网页下载处理
class HtmlDownloader(object):
    def download(self, url):
        response = urllib2.urlopen(url)
        if response.getcode() != 200:
            return None
        return response.read()
#网页解析处理
class HtmlParser(object):
    def parse(self, page_url, html_cont,name):
        if html_cont is None:
            return None
        else:
            soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
            nov_times = self._get_nov_time()
            self._get_new_data(page_url, soup,name,nov_times)
            return nov_times

    def _get_nov_time(self):
        nov_time = datetime.datetime.now()
        return nov_time

    def _get_new_data(self, page_url, soup,name,times):
        title_node = soup.find('title')
        table_node = soup.find_all('table')
        for table in table_node:
            new_test = userdata(name=name,url = page_url,title = title_node.get_text(),time = times,date = table.prettify())
            new_test.save()

#主程序处理
class SpiderMain(object):
    def __init__(self):
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()

    def craw(self, root_url,name):
        try:
            html_cont = self.downloader.download(root_url)
            nov_times = self.parser.parse(root_url, html_cont,name)
            return nov_times
        except:
            print "craw failed!"

