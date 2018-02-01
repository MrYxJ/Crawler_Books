#!/usr/bin/env python
#coding:UTF-8

import os
import re
import sys
import markdown
import codecs
import time
import pdfkit
import requests
from bs4 import BeautifulSoup

class crawler_book():
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
    {content}
    </body>
    </html>
    """
    UserAgent = 'User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
    header = {'User-Agent': UserAgent}
    css = '''
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <style type="text/css">
    <!-- 此处省略掉markdown的css样式，因为太长了 -->
    </style>
    '''

    def get_html_text(url):
        try:
            response = requests.get(url,headers =header,timeout=300)
            response.raise_for_status()
            print('Result code:',response.status_code)
            response.encoding = 'utf-8'
            return response.text
        except:
            print('Error:',response.status_code)
            return None

    def clean(s):
        s = s.replace('\n','')
        s = s.replace(' ','')
        return s

    def crawler_list(url, html = None):
        '''
         从某个网页，获取返回要爬取所有链接
        :param html: 传入一个含有爬取所有链接网页
        :return:
        '''
        pass

    def relative_to_positive_url(m, url_home):
        '''
        根据主站
        :param url_home:
        :return:
        '''
        if not m.group(2).startswith("http"):
            rtn = "".join([m.group(1), url_home, m.group(2), m.group(3)])
            return rtn
        else:
            return "".join([m.group(1), m.group(2), m.group(3)])

    def analy_body(html):
        pass

    def find_name(url): #找到该网页资源名字
        return re.search(r'(content/)([\s|\S]*.html|)',url).group(2)

    def url_to_file(ulist):#前一到七章
        pass

    def html_to_pdf(ulist,file_name):
        """
            把所有html文件转换成pdf文件
        """
        pass

    def markdown_to_html(ulist):
        pass

    def printlist(ulist):
        for i in range(len(ulist)):
            print(ulist[i])

    def write(ulist,name):
        with open(name,'w') as f:
            for line in ulist:
                f.writelines(line+'\n')

    def read(name):
        ulist = []
        with open(name,'r') as f:
           for line in f.readlines():
               line = line[:-1]
               ulist.append(line)
        return ulist


