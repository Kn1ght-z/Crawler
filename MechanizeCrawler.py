#!/usr/bin/env python
#coding=utf-8
'''
    python爬虫 : mechanize
'''
import mechanize
import cookielib
import traceback
import sys
import urllib 

reload(sys) 
sys.setdefaultencoding('utf8')

class MechanizeCrawler(object):
    
    def __init__(self, headers = {}, debug = True, p = ''):
        self.timeout = 10  
        self.br = mechanize.Browser() #初始化br
        self.cj = cookielib.LWPCookieJar()
        self.br.set_cookiejar(self.cj)#关联cookie
        self.br.set_handle_equiv(True)#是否处理http equiv
        self.br.set_handle_gzip(True)#是否自动解压
        self.br.set_handle_redirect(True)#是否支持重定向
        self.br.set_handle_referer(True)#是否自动添加referer
        self.br.set_handle_robots(False)#是否遵循robots协议
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        self.br.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')]
        self.debug = debug
        #debug方便看到中间过程，便于调试
        if self.debug:
            self.br.set_debug_http(True)
            self.br.set_debug_redirects(True) 
            self.br.set_debug_responses(True)
        #headers
        for keys in headers.keys():
            self.br.addheaders += [(key, headers[key]), ]
        #proxy
        if len(p) > 0 and p != 'None' and p != None and p != 'NULL':
            self.br.set_proxies({'http': p})
    
    def _replace(self,key):
        cur=0
        for header in self.br.addheaders:
            if header[0]==key:
                return cur
            cur+=1
        return -1

    # add referer 
    def add_referer(self, referer):
        cur=self._replace('Referer')
        if cur!=-1:
            self.br.addheaders.pop(cur)
        self.br.addheaders+=[('Referer',referer),]
    
    # add header 
    def add_header(self, headers = {}):
        for key in headers:
            cur=self._replace(key)
            if cur!=-1:
                self.br.addheaders.pop(cur)
            self.br.addheaders += [(key, headers[key]), ]

    # set proxy 
    def set_proxy(self, p):
        self.br.set_proxies({'http': p})

    # get
    def get(self, url, html_flag = False,headers_flag = False):
        html = ''
        headers = {}
        try:

            resp = self.br.open(url, timeout = self.timeout)
            if html_flag:
                html = resp.get_data()
            if headers_flag:
                headers = resp.info()
        except Exception, e:
            if self.debug:
                print e

        return html , headers

    # post
    def post(self, url, paras = {}, html_flag = False,headers_flag = False):
        html = ''
        headers = {}
        try:
            resp = self.br.open(url, data = urllib.urlencode(paras), timeout = self.timeout)
            if html_flag:
                html = resp.get_data()
            if headers_flag:
                headers = resp.info()
        except Exception, e:
            if self.debug:
                print e

        return html , headers

if __name__ == '__main__':

    username = "xxxxx"
    password = "xxxxx"
    try:
        headers={
            "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }
        br = MechanizeCrawler(debug=True)
        br.add_header(headers)
        #home
        home_url = "https://leetcode.com/"
        page1 , headers1=br.get(home_url,html_flag=True,headers_flag = True)
        cookies = headers1["Set-Cookie"]
        csrftoken = cookies.split(";")[0].split("=")[1]
        #login
        login_url = "https://leetcode.com/accounts/login/"
        paras = {
            "csrfmiddlewaretoken":csrftoken,
            "login": username,
            "password":password
        }
        br.add_referer(home_url)
        page2, headers2= br.post(login_url, paras = paras, html_flag =True, headers_flag = True)
        print page2
        print headers2
    except Exception, e:
        #raise e
        traceback.print_exc()  
   
    
   