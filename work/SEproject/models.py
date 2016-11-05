# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import urllib2
from bs4 import BeautifulSoup

# Create your models here.
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
        res_data = {}
        list_table = []
        title_node = soup.find('title')
        res_data['title'] = title_node.get_text()
        table_node = soup.find_all('table')
        for table in table_node:
            list_table.append(table.prettify())
        res_data['table'] = list_table
        return res_data

class HtmlOutputer(object):

    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        fout = open('output.html', 'w')
        fout.write("<html>")
        fout.write("<body>")
        fout.write("<table>")
        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td>%s</td>" % data['title'].encode('utf-8'))
            fout.write("</tr>")
            leng = len(data['table'])
            for i in range(0,leng-1):
                fout.write("<tr>")
                fout.write("<td>%s</td>" % data['table'][i])
                fout.write("</tr>")
        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
        fout.close()

class SpiderMain(object):
    def __init__(self):
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.outputer = HtmlOutputer()

    def craw(self, root_url):
        try:
            print 'craw : %s' % (root_url)
            html_cont = self.downloader.download(root_url)
            new_data = self.parser.parse(root_url, html_cont)
            self.outputer.collect_data(new_data)
        except:
            print 'craw failed'
        self.outputer.output_html()


