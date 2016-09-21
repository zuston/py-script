# -*- coding:utf-8 -*-

import time
import requests
from bs4 import BeautifulSoup

_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Cache-Control": "max-age=0",
    "Host": "www.xicidaili.com",
    "Referer": "http://www.xicidaili.com/nn/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
}

_cookies = ""

def spider(total_page,_cookies):
    url = "http://www.xicidaili.com/nn/"
    for i in range(1, total_page):
        if i % 100 == 0:
            # 100个页面更新一次Cookie
            _cookies = requests.get("http://www.xicidaili.com/", headers=_headers).cookies
        r = requests.get(url + str(i), headers=_headers, cookies=_cookies)
        html_doc = r.text
        parseDate(html_doc)
        status_code = r.status_code
        print i, status_code
        r.close()

        # with open("%s.html" % i, "w") as f:  # 保存html，也可以直接信息提取
        #     f.write(html_doc.encode("utf-8"))
        time.sleep(1)
        _headers["Referer"] = url + str(i - 1)
        exit(1)

def parseDate(html):
    ip_data = []
    soup = BeautifulSoup(html)
    group = soup.find_all("tr",class_="odd")
    for onedata in group:
        temp=[]
        ip = (onedata.find_all("td"))[1].string
        port = (onedata.find_all("td"))[2].string
        print "IP:%s\tPort:%s"%(ip,port)
        ip_data.append(zip(ip,port))
    return ip_data

if __name__ == "__main__":
    _cookies = requests.get("http://www.xicidaili.com/", headers=_headers).cookies
    spider(200,_cookies)