# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import urllib2
from bs4 import BeautifulSoup
import datetime
# Create your models here.
class testhtml(models.Model):
    url = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    time = models.DateTimeField()
    date = models.TextField()
# 网页下载
class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None
        response = urllib2.urlopen(url)
        if response.getcode() != 200:
            return None
        return response.read()

class HtmlParser(object):
    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_data = self._get_new_data(page_url, soup)
        return new_data

    def _get_new_data(self, page_url, soup):
        title_node = soup.find('title')
        print title_node.get_text()
        print datetime.datetime.now()
        print page_url
        #table_node = soup.find_all('table')
        print str(soup.table)
        #for table in table_node:
            #print str(table)
        #models.testhtml.objects.create(url = page_url,title = title_node.get_text(),time = datetime.datetime.now(),date = str(soup.table))
        new_test = testhtml(url = page_url,title = title_node.get_text(),time = datetime.datetime.now(),date = str(soup.table))
        new_test.save()
        #models.testhtml.save()
        #p.save()
        #print p.id



class SpiderMain(object):
    def __init__(self):
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()

    def craw(self, root_url):
        try:
            #print 'craw : %s' % (root_url)
            html_cont = self.downloader.download(root_url)
            new_data = self.parser.parse(root_url, html_cont)
        except:
            print 'craw failed'


