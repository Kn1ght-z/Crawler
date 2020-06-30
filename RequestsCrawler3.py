#!/usr/bin/env python
#coding=UTF8
'''
    @desc: 爬虫基础模块
'''
import requests
import traceback
import datetime
import sys
from lxml import html
import re

class RequestsCrawler(object):

    def __init__(self, headers = {},debug = True, p = ''):
        self.timeout = 30
        self._allow_redirects = True
        self._verify = True
        self.debug = debug
        self.headers = {
            'User-Agent':'Mozilla/5.1 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
        }
        #headers
        self.headers.update(headers)
        #proxy
        self.proxies = {}
        if p != '':             
            self.proxies = { 
                'http':p,
                'https':p
            }

        self.s = requests.Session()

    #set debug
    def set_debug(self,debug):
        self.debug = debug

    #add referer
    def add_referer(self, referer):
        if referer != None and referer != '':
            self.headers.update({'Referer':referer})

    #add header
    def add_header(self, headers = {}):
        self.headers.update(headers)

    #set proxy
    def set_proxy(self, p = ''):
        if p != '':             
            self.proxies = {
                'http':p, 
                'https':p
            }

    #get
    def get(self, url):
        try:
            r = ""
            if self.debug:
                print ('get : '+url)
            req = requests.Request('GET', url, headers = self.headers)
            prepped = self.s.prepare_request(req)
            r=self.s.send(prepped, proxies = self.proxies,allow_redirects = self._allow_redirects,verify = self._verify,timeout = self.timeout)
            if self.debug:
                if len(r.history) != 0:
                    #whether redirect or not
                    for _r in r.history:
                        print('request : '+ _r.url)
                        for header in _r.request.headers:
                            print('request : '+header+' : '+_r.request.headers[header])
                        print ('')
                        print ('replay :'+str(_r.status_code))
                        for header in _r.headers:
                            print ('response : '+header+' : '+_r.headers[header])
                    print ('')
                print('request : '+ r.url)
                for header in r.request.headers:
                    print ('request : '+header+' : '+r.request.headers[header])
                print ('')
                print('reploy :'+str(r.status_code))
                for header in r.headers:
                    print ('response : '+header+' : '+r.headers[header])
        except Exception as e:
            if self.debug:
                print (e)
                #traceback.print_exc()
        return r

    #post
    def post(self, url, paras = {}):
        try:
            r = ""
            if self.debug:
                print ('post : '+url),
                if len(paras):
                    print (paras)     
            req = requests.Request('POST', url,data=paras,headers=self.headers)
            prepped = self.s.prepare_request(req)
            r = self.s.send(prepped, proxies = self.proxies,allow_redirects = self._allow_redirects,verify = self._verify,timeout = self.timeout)
            
            if self.debug:
                if len(r.history) != 0:
                    #whether redirect or not
                    for _r in r.history:
                        print ('request : '+ _r.url)
                        for header in _r.request.headers:
                            print ('request : '+header+' : '+_r.request.headers[header])
                        print ('')
                        print ('replay :'+str(_r.status_code))
                        for header in _r.headers:
                            print ('response : '+header+' : '+_r.headers[header])
                    print ('')
                print ('request : '+ r.url)
                for header in r.request.headers:
                    print ('request : '+header+' : '+r.request.headers[header])
                print ('')
                print ('replay :'+str(r.status_code))
                for header in r.headers:
                    print ('response : '+header+' : '+r.headers[header]) 
        except Exception as e:
            if self.debug:
                print (str(e))
                #traceback.print_exc()
        return r 


if __name__ == '__main__':
    br = RequestsCrawler(debug=True)
    headers={
        "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }
    br.add_header(headers)
    url = "xxxxxxx"
    res= br.get(url)
    try:
        print (res.headers)
        res.encoding = 'gb2312' 
        page =  res.text
    except Exception as e:
        page =  res.content.decode("gb2312").encode('utf-8')
    #print page

   