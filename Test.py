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

URL = "https://germey.gitbooks.io/python3webspider/content/"
UserAgent = 'User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
header = {'User-Agent':UserAgent}

def getHtmlText(url):
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

def CrawleList(url,html = None): #根据侧边目录爬取所有要爬的网页的目录
    html = getHtmlText(url)
    soup = BeautifulSoup(html,'html.parser')
    ulist1 = [] #前1~7章 html
    ulist2 = [] #后8~15章 md
    test = soup.select('.chapter')
    cnt = 1
    flag = False
    for li in test:
        Str = clean(li.a.string)
        if Str.find("第八章") >= 0:  flag = True
        if  Str.find("第")>=0 :
            index = Str.find("章")
            Str = str(cnt)+'-'+Str[index+1:]
            cnt += 1
        if flag == False:
            ulist1.append(Str+'.html')
        else:
            ulist2.append(Str+'.md')
    ulist1[0] = ''
    ulist1[1] = '0-'+ulist1[1]
    for i in range(len(ulist1)):
        ulist1[i] = url + ulist1[i]
    for i in range(len(ulist2)):
        ulist2[i] = url + ulist2[i]
    return ulist1,ulist2

def func(m):
    if not m.group(2).startswith("http"):
        rtn = "".join([m.group(1),URL, m.group(2), m.group(3)])
        return rtn
    else:
        return "".join([m.group(1), m.group(2), m.group(3)])

def AnalyBody(html):
    try:
        soup = BeautifulSoup(html,'lxml')
        body = soup.select('.search-noresults')[0]
        html = str(body)
        pattern = "(<img .*?src=\")(.*?)(\")"
        html = re.compile(pattern).sub(func,html)
        html = html_template.format(content=html)
        html = html.encode("utf-8")
        return html
    except Exception as e:
        print('Erro Information: ',e)
        return None

def Find(url):
    return re.search(r'(content/)([\s|\S]*.html|)',url).group(2)

def url_to_file(ulist):#前一到七章
    start = time.time()
    htmls = []
    for index, url in enumerate(ulist):
        try:
            html = AnalyBody(getHtmlText(url))
            f_name = Find(url)
            if f_name == '' : f_name = '.html'
            with open(f_name, 'wb') as f:
                f.write(html)
                htmls.append(f_name)
        except Exception as e:
            print('Error Information:',e,'\n  Error Url:',url)
            continue
    total_time = time.time() - start
    print(u"总共耗时：%f 秒" % total_time)
    return htmls

def html_to_pdf(ulist,file_name):
    """
        把所有html文件转换成pdf文件
    """
    htmls = []
    for index, url in enumerate(ulist):
        f_name = Find(url)
        if f_name == '': f_name = '.html'
        htmls.append(f_name)
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'cookie': [
            ('cookie-name1', 'cookie-value1'),
            ('cookie-name2', 'cookie-value2'),
        ],
        'outline-depth': 10,
    }
    start = time.time()
    print('开始html转换成pdf......')
    pdfkit.from_file(htmls,file_name+'.pdf')
    total_time = time.time() - start
    print(u"总共耗时：%f 秒" % total_time)

css = '''
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style type="text/css">
<!-- 此处省略掉markdown的css样式，因为太长了 -->
</style>
'''

def markdown_to_html(ulist):
    markdowns =[]
    for index,url in enumerate(ulist):
        f_name = Find(url)
        markdowns.append(f_name)
    for address in ulist:
        input_file = codecs.open(address, mode="r", encoding="utf-8")
        text = input_file.read()
        html = markdown.markdown(text)
        final_address =''
        output_file = codecs.open(final_address, "w", encoding="utf-8", errors="xmlcharrefreplace")
        output_file.write(css + html)

def printlist(ulist):
    for i in range(len(ulist)):
        print(ulist[i])

def run():
    pass

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


if __name__ == '__main__':
    #ulist1,ulist2 = CrawleList(URL)
    #write(ulist1,'ulist1.txt')
    #write(ulist2,'ulist2.txt')
    ulist1 = read("ulist1.txt")
    #htmls = url_to_file(ulist1)
    html_to_pdf(ulist1,'Python3网络爬虫实战')

