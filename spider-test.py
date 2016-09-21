# -*- coding:utf-8 -*-

import urllib
import urllib2
import sys
import gzip
import requests
import commands
import os
from StringIO import StringIO
import time
from bs4 import BeautifulSoup as bs
import random

reload(sys)
sys.setdefaultencoding("utf8")

pageIndex = 9
proxyIpFlag = 0
ip2port = ''
page = 1

def postValue(searchContent, startYear, endYear):
    global proxyIpFlag
    global  ip2port
    url = "http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showSearchResult-startWa.shtml";
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36';

    searchKeyWords = expandString(searchContent)
    executableSearchExp = "VDB:(IBI='" + searchContent + "' AND (APD>=" + startYear + " AND APD<=" + endYear + "))"
    searchExp = "复合申请人与发明人=(" + searchContent + ")"
    resexecutableSearchExp = "VDB:(IBI='" + searchContent + "')"
    dataExecutableSearchExp = "AND (APD>=" + startYear + " AND APD<=" + endYear + ")"

    values = {
        'searchCondition.searchType': 'Sino_foreign',
        'searchCondition.searchKeywords[]': searchKeyWords,
        'searchCondition.executableSearchExp': executableSearchExp,
        'searchCondition.searchExp': searchExp,
        "searchCondition.resultMode": "SEARCH_MODE",
        'searchCondition.sortFields': '-APD,+PD',
        "resultPagination.limit": 1,
        "resultQC.executableSearchExp": resexecutableSearchExp,
        "resultQC.dataExecutableSearchExp": dataExecutableSearchExp,
        "wee.bizlog.modulelevel": "0200603",
    }
    headers = {'User-Agent': user_agent}
    data = urllib.urlencode(values)


    if(proxyIpFlag==1):
        proxy_handler = urllib2.ProxyHandler({"http" : ip2port})
        print "当前代理",ip2port
        opener = urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)

    request = urllib2.Request(url, data, values)
    try:
        response = urllib2.urlopen(request, timeout=15)
        # print response.info().get('Content-Encoding')
        pageEncoding = response.info().get('Content-Encoding')
        resData = ''
        data = response.read()
        print "(+)正在解析......"
        if pageEncoding == 'gzip':
            buf = StringIO(data)
            f = gzip.GzipFile(fileobj=buf)
            resData = f.read()
        else:
            resData = data

        soup = bs(resData)
        count = soup.select("input #result_totalCount")
        IpFlag = soup.select("div #error_msg")
        # print IpFlag[0].h3.string.strip()
        if count != []:
            print searchContent, "在", startYear, "到", endYear, "期间总计专利数:", count[0].get("value")
            return count[0].get("value")
        elif len(IpFlag) == 1:
            # print "-------------------------------"
            # print IpFlag[0].h3.string.strip()
            # print "================================"
            # print "等待重启pppoe,切换ip"
            # (status1,out1) = commands.getstatusoutput("networksetup -disconnectpppoeservice PPPoE")
            # (status2,out2) = commands.getstatusoutput("networksetup -connectpppoeservice PPPoE")
            # if status1==0 and status2==0:
            #     print "(+)切换ip  成功  !!!"
            # else:
            #     print '(-)切换ip失败'
            #     exit(1)

            # proxyIpFlag = 1
            # ip2port = getProxyIp()[0]+":"+getProxyIp()[1]
            # print ip2port
            return -2
            # exit(1)

        else:
            print soup.title.string
            if soup.title.string == "404啦-页面没找哦，亲":
                print resData
                exit(1)
            print searchContent, "在", startYear, "到", endYear, "期间总计专利数:", "未查到有关专利信息"
            return 0
    except Exception:
        print "超时"
        # exit(1)
        return -2


def expandString(string):
    string = string.decode('utf-8')
    resStr = ''
    for s in string:
        # print s
        resStr += "[" + s + "][ ]{0,}"
    return resStr


def readExcel():
    import xlrd
    book = xlrd.open_workbook("patent10.xlsx", encoding_override='utf-8')
    sh = book.sheet_by_index(pageIndex)
    # print sh.name
    # print sh.nrows
    # print sh.ncols
    array = []
    tag_row = 1
    array.append([0, tag_row])
    for rx in range(1, sh.nrows):
        # print dir((sh.row(rx))[0])
        cid = str(((sh.row(rx))[0].value))
        cid = cid[:-2]
        cname = ((sh.row(rx))[2]).value
        if str(((sh.row(rx))[3].value)) != '' or str(((sh.row(rx))[4].value)) != '' or str(
                ((sh.row(rx))[5].value)) != '' or str(((sh.row(rx))[6].value)) != '' or str(
                ((sh.row(rx))[7].value)) != '':
            tag_row = rx + 1
            array[0] = [0, tag_row]
        else:
            array.append([cid, cname])
        # array.append([cid, cname])
    return array


def writeExcel(resArray, tag_row):
    import xlrd
    from xlutils.copy import copy

    rb = xlrd.open_workbook("patent10.xlsx")

    # 通过sheet_by_index()获取的sheet没有write()方法
    rs = rb.sheet_by_index(2)
    wb = copy(rb)

    # 通过get_sheet()获取的sheet有write()方法
    ws = wb.get_sheet(pageIndex)
    count = tag_row
    i = 0
    for data in resArray:
        ws.write(count, 3 + i, data)
        i = i + 1
    wb.save('patent10.xlsx')


def action():
    array = readExcel()
    # resRes = []
    tag_row = 1
    count = 0
    for cyear, cname in array:
        if count == 0:
            print "采集数据位置:", cname
            tag_row = cname
            count += 1
        else:
            cintYear = int(cyear)
            f5y = cintYear - 5
            f1y = cintYear - 1
            z0y = cintYear
            z1y = cintYear + 1
            z2y = cintYear + 2

            yearArray = [f5y, f1y, z0y, z1y, z2y]
            oneCompanyRes = []
            threhold = 0
            for year in yearArray:
                date = postValue(cname, appendYearString(year)[0], appendYearString(year)[1])
                # 做判断,能否成功抓取
                date = loopPost(date,cname,appendYearString(year)[0],appendYearString(year)[1])
                time.sleep(threhold)
                oneCompanyRes.append(date)

            print "正在放入缓存list:当前位置:%d"%tag_row
            # writeExcel(oneCompanyRes, tag_row)
            tag_row += 1
            count += 1
            print ''

    print "已经结束"

def loopPost(data,cname,startYear,endYear):
    if(data==-2):
        global proxyIpFlag
        proxyIpFlag = 1
        global ip2port
        ip2port = getProxyIp()[0] + ":" + getProxyIp()[1]
        print ip2port
        data = postValue(cname, startYear, endYear)
        return loopPost(data,cname,startYear,endYear)
    else:
        return data

def appendYearString(year):
    start = str(year) + ".01.01"
    end = str(year) + ".12.31"
    return [start, end]


def getProxyIp():
    global page
    ip = ""
    port = ""
    _headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "max-age=0",
        "Host": "www.xicidaili.com",
        "Referer": "http://www.xicidaili.com/nn/"+str(page-1),
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
    }
    _cookies = ""

    url = "http://www.xicidaili.com/nn/"

    _cookies = requests.get("http://www.xicidaili.com/", headers=_headers).cookies
    r = requests.get(url + str(page), headers=_headers, cookies=_cookies)
    html_doc = r.text

    status_code = r.status_code
    groupData = parseDate(html_doc)
    # print status_code
    # print groupData
    r.close()

    # _headers["Referer"] = url + str(i - 1)
    # 验证ip可用性
    for key,value in groupData:
        # print key,value
        proxy_handler = urllib2.ProxyHandler({"http" : '%s:%s'%(key,value)})
        opener = urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)
        # time1 = time.time()

        try:
            request = urllib2.Request("http://www.baidu.com")
            response = urllib2.urlopen(request, timeout=3)
            ip = key
            port = value
            break;
        except Exception:
            print "(+)正在测试抓起代理ip-------"
            continue
    page = random.randint(1,2)
    print page
    return (ip,port)

def parseDate(html):
    ip_data = []
    soup = bs(html)
    group = soup.find_all("tr", class_="odd")
    for onedata in group:
        temp = []
        ip = (onedata.find_all("td"))[1].string
        port = (onedata.find_all("td"))[2].string
        # print "IP:%s\tPort:%s" % (ip, port)
        ip_data.append([ip,port])
    return ip_data


if __name__ == "__main__":
    action()
    # print getProxyIp()