
## * 说明

爬虫主要用来抓取网页数据，包括`数据抓取`和`数据解析` 两个方面，而python在爬虫的实现上提供了多种可选的类库，其中：
  
  * 数据抓取：

   - urllib2/urllib3 
   - requests 
   - mechanize
   - selenium 
   - splinter
  
* 数据解析：

  - lxml 
  - beautifulsoup4


* 对于数据抓取，涉及的过程主要是向服务器发送构造好的http请求，常见类型有：get / post。
    * urllib2/urllib3 、requests 、mechanize、httplib用来获取原始的静态响应页面;
    * selenium、splinter可通过加载浏览器驱动获取动态页面内容，处理ajax，模拟程度更高;
    * 具体选择使用哪种类库，应根据实际需求决定;
  
  
* 对于数据解析，主要是从响应页面里提取所需的数据，常用方法有：xpath路径选择器,css选择器,正则表达式。


## * 目的

本模块是为了对爬虫数据抓取有关的已有类库（urllib2、requests、mechanize）进行再次封装，对外提供简洁的接口。

## * 功能：

* 支持
    - get/post请求
    - debug模式
    - 自处理重定向
    - 保持cookie
    - 设置代理
    
## *其它
  使用方法可参考主函数中用例 
