#!/usr/bin/env python
#coding=utf-8
'''
    python爬虫 : urllib2
'''
import urllib
import urllib2
import cookielib
import traceback
import sys

reload(sys) 
sys.setdefaultencoding('utf8')

class UrllibCrawler(object):

    def __init__(self, headers = {},debug = True, p = ''):
        #timeout 
        self.timeout = 10
        #cookie handler
        self.cookie_processor = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
      
        #debug handler
        self.debug = debug
        if self.debug:
            self.httpHandler = urllib2.HTTPHandler(debuglevel=1)
            self.httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
        else:
            self.httpHandler = urllib2.HTTPHandler(debuglevel=0)
            self.httpsHandler = urllib2.HTTPSHandler(debuglevel=0)
         
        #proxy handler (http)
        if p != '' and p != 'None' and p != None and p != 'NULL':
            self.proxy_handler = urllib2.ProxyHandler({'http': p})
        else:
            self.proxy_handler = urllib2.ProxyHandler({})
 
        #opener
        self.opener = urllib2.build_opener( self.cookie_processor,self.proxy_handler, self.httpHandler, self.httpsHandler)
        self.opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'),]
       
        #header
        for key in headers.keys():
            cur=self._replace(key)
            if cur!=-1:
                self.opener.addheaders.pop(cur)
            self.opener.addheaders += [(key, headers[key]), ]
    
    def _replace(self,key):
        cur=0
        for header in self.opener.addheaders:
            if header[0]==key:
                return cur
            cur+=1
        return -1

    #add referer
    def add_referer(self, referer):
        cur=self._replace('Referer')
        if cur!=-1:
            self.opener.addheaders.pop(cur)
        self.opener.addheaders+=[('Referer',referer),]
    
    #add header
    def add_header(self, headers = {}):
        for key in headers.keys():
            cur=self._replace(key)
            if cur!=-1:
                self.opener.addheaders.pop(cur)
            self.opener.addheaders += [(key, headers[key]), ]

    #get
    def get(self, url, html_flag = False, headers_flag = False):
        html = ''
        headers = {}
        try:
            print '#get'
            print url
            resp = self.opener.open(url,timeout=self.timeout)
            if html_flag:
                html = resp.read()
            if headers_flag:
                headers = resp.headers
        except Exception, e:
            if self.debug:
                print e

        return html, headers

    #post
    def post(self, url, paras = {}, html_flag = False, headers_flag = False):
        html = ''
        headers = {}
        try:
            print '#post'
            print url
            req = urllib2.Request(url)  
            datas = urllib.urlencode(paras) 
            resp = self.opener.open(req, datas,timeout=self.timeout)
            if html_flag:
                html = resp.read()
            if headers_flag:
                headers = resp.headers
        except Exception, e:
            if self.debug:
                print e
        print  headers
        return html, headers


if __name__ == '__main__':
    
    username = "xxxxx"
    password = "xxxxx"
    try:
        headers={
            "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }
        br = UrllibCrawler(debug=True)
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
        page2, headers2= br.post(login_url, paras = paras, html_flag =True,headers_flag = True)
        print page2
        print headers2

    except Exception, e:
        #raise e
        traceback.print_exc()  

    
    
   