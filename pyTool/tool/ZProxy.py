#! -*- coding:utf8 -*-
import os
import sys
import redis
sys.path.append('..')
import config.DbConfig as config
from bs4 import BeautifulSoup as bs
import Http
import config.DbConfig as config

class ZProxy(object):
    def __init__(self):
        self.proxyName = config.redisDict['proxyName']
        self._getRedisConn()

    def _getRedisConn(self):
        self.redisConn = redis.StrictRedis(host=config.redisDict['host'],port=config.redisDict['port'])

    def _parseDate(self,html):
        ip_data = []
        soup = bs(html)
        group = soup.find_all("tr", class_="odd")
        for onedata in group:
            temp = []
            ip = (onedata.find_all("td"))[1].string
            port = (onedata.find_all("td"))[2].string
            # print "IP:%s\tPort:%s" % (ip, port)
            ip_data.append(ip+":"+port)
        return ip_data

    def _getProxyIp2Pool(self):
        # 维持一个代理池，采用的是西祠的透明代理
        hp = Http.Http()
        _headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Host": "www.xicidaili.com",
            "Referer": "http://www.xicidaili.com/nt/1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
        }
        url = "http://www.xicidaili.com/nt/"

        code,msg,page = hp.open(url,**_headers)
        if code!=200:
            print "can not get the ip"
            return False

        resList = self._parseDate(page)
        for r in resList:
            self.redisConn.sadd(self.proxyName,r)
        return True



    def getIp(self):
        count = self.redisConn.scard(self.proxyName)
        if count <= 1 or count is None:
            self._getProxyIp2Pool()
            return self.getIp()
        else:
            proxyIP = self.redisConn.spop(self.proxyName)
            return proxyIP

    def flushPool(self):
        pass

if __name__ == '__main__':
    proxy = ZProxy()
    print proxy.getIp()
