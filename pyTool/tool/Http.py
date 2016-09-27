# -*- coding:utf-8 -*-
import urllib2
import urllib
import gzip
from StringIO import StringIO
import sys
import time
import ZProxy as proxy
reload(sys)
sys.setdefaultencoding("utf8")

class Http(object):

    def __init__(self):
        self.proxyFlag = False

    def _openProxy(self):
        self.proxyFlag = True

    def _closeProxy(self):
        self.proxyFlag = False

    def costTimeDec(func):
        def wrapper(*args,**kw):
            startTime = time.time()
            res = func(*args,**kw)
            endtime = time.time()
            costTime = endtime-startTime
            print 'the spider process cost is:',costTime
            return res
        return wrapper

    def proxyDec(proxyFlag):
        def decorate(func):
            def wrapper(*args,**kw):
                if proxyFlag:
                    pass
                return func(*args,**kw)
            return wrapper
        return decorate


    @costTimeDec
    def _request(self,url,postValue=None,**headers):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36';
        if not headers:
            headers = {'User-Agent': user_agent}
        else:
            if 'User-Agent' not in headers:
                headers['User-Agent'] = user_agent
        if postValue is not None:
            postData = urllib.urlencode(postValue)
            request = urllib2.Request(url, postData, headers)
        else:
            request = urllib2.Request(url,headers=headers)

        if self.proxyFlag:
            # need to spider the proxyIp
            proxyIp = self._getProxyIp()
            proxy_handler = urllib2.ProxyHandler({'http':proxyIp})
            urllib2.install_opener(urllib2.build_opener(proxy_handler))

        try:
            response = urllib2.urlopen(request,timeout=10)
            code = response.getcode()
            resMsg = response.msg
            pageEncoding = response.info().get('Content-Encoding')
            page = response.read()
            if pageEncoding == 'gzip':
                buf = StringIO(page)
                f = gzip.GzipFile(fileobj=buf)
                page = f.read()

            return [code,resMsg,page]
        except Exception:
            code = -2
            resMsg = 'out of time'
            page = None
            return [code,resMsg,page]

    def _getProxyIp(self):
        proxyPool = proxy.ZProxy()
        ip = proxy.getLastedIp()
        return ip


    def post(self,url,postValue,**headers):
        return self._request(url,postValue,**headers)

    def open(self,url,**headers):
        return self._request(url,**headers)




# 缺少代理挂载

if __name__ == '__main__':
    http = Http()
    code,resMsg,page = http.open('http://www.zhihu.com',
                    Cookie = 'd_c0="AEAAHF7tUgqPTser6aQFFNucOrpy_pVS_nM=|1470143843"; _zap=e0aa3eeb-4a2f-469a-b0c0-213999c8fad8; q_c1=9b67681f980240caad14cf09153f8cf4|1472825844000|1470143841000; l_cap_id="MjAyZjk4OWRkNWViNDg3NDk0Y2EzZDY3Y2RjNzMwN2Q=|1473305517|5e44a389c8a8d1c492f8e28b6c33558684f9709b"; cap_id="NWVjNTlmODg0ZjA0NDNjNmFjZjczYzVkOGE1NDVlOWM=|1473305517|483c89cfd8b6a38c9dfa3e64ca36874c5b1fc7f6"; login="ZWVhYzM3MDk5ZjMzNDdjOTlhYzc2OThiMzM1M2E2Yzg=|1473305538|b24862947894611df60da385d5321c7152828405"; __utmt=1; __utma=51854390.1478424689.1473601532.1474426191.1474436825.11; __utmb=51854390.3.9.1474436838115; __utmc=51854390; __utmz=51854390.1474436825.11.11.utmcsr=baidu.com|utmccn=(referral)|utmcmd=referral|utmcct=/index.php; __utmv=51854390.100-1|2=registration_date=20131021=1^3=entry_date=20131021=1; a_t="2.0AAAAmHsfAAAXAAAA5KsJWAAAAJh7HwAAAEAAHF7tUgoXAAAAYQJVTcJo-FcAPd0Msxz2C-lOeeikr99GzbSowiV5bg9W3imFV1LlbeAWXvSVBCxarA=="; z_c0=Mi4wQUFBQW1Ic2ZBQUFBUUFBY1h1MVNDaGNBQUFCaEFsVk53bWo0VndBOTNReXpIUFlMNlU1NTZLU3YzMGJOdEtqQ0pR|1474436836|6bf62efd8b544ab5415eda5bd7a08201827a15ac')
    print code
