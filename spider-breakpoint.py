# -*- coding:utf-8 -*-

import urllib
import urllib2
import sys
import gzip
import commands
import os
from StringIO import StringIO
import time
from bs4 import BeautifulSoup as bs
reload(sys)
sys.setdefaultencoding("utf8")


def postValue(searchContent,startYear,endYear):
    url = "http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showSearchResult-startWa.shtml";
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36';

    searchKeyWords = expandString(searchContent)
    executableSearchExp = "VDB:(IBI='"+searchContent+"' AND (APD>="+startYear+" AND APD<="+endYear+"))"
    searchExp = "复合申请人与发明人=("+searchContent+")"
    resexecutableSearchExp = "VDB:(IBI='"+searchContent+"')"
    dataExecutableSearchExp = "AND (APD>="+startYear+" AND APD<="+endYear+")"

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

    # proxy_handler = urllib2.ProxyHandler({"http" : '122.96.59.104:80'})
    # opener = urllib2.build_opener(proxy_handler)
    # urllib2.install_opener(opener)
    request = urllib2.Request(url, data, values)
    try:
        response = urllib2.urlopen(request, timeout=10)
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
            print searchContent,"在",startYear,"到",endYear,"期间总计专利数:", count[0].get("value")
            return count[0].get("value")
        elif len(IpFlag) ==1:
            print "-------------------------------"
            print IpFlag[0].h3.string.strip()
            print "================================"
            print "等待重启pppoe,切换ip"
            (status1,out1) = commands.getstatusoutput("networksetup -disconnectpppoeservice PPPoE")
            (status2,out2) = commands.getstatusoutput("networksetup -connectpppoeservice PPPoE")
            if status1==0 and status2==0:
                print "(+)切换ip  成功  !!!"
            else:
                print '(-)切换ip失败'
                exit(1)

        else:
            print searchContent,"在",startYear,"到",endYear,"期间总计专利数:","未查到有关专利信息"
            return 0
    except urllib2.URLError:
        print "超时"
        return -1

def expandString(string):
    string = string.decode('utf-8')
    resStr = ''
    for s in string :
        # print s
        resStr += "["+s+"][ ]{0,}"
    return resStr

def readExcel():
    import xlrd
    book = xlrd.open_workbook("0815patent.xlsx", encoding_override='utf-8')
    sh = book.sheet_by_index(1)
    # print sh.name
    # print sh.nrows
    # print sh.ncols
    array = []
    tag_row = 1
    array.append([0,tag_row])
    for rx in range(1, sh.nrows):
        # print dir((sh.row(rx))[0])
        cid = str(((sh.row(rx))[0].value))
        cid = cid[:-2]
        cname = ((sh.row(rx))[2]).value
        # print cid
        # print cname
        if str(((sh.row(rx))[3].value))!='':
            tag_row = rx+1
            array[0] = [0,tag_row]
        else:
            array.append([cid,cname])
    return array

def writeExcel(resArray,tag_row):
    import xlrd
    from xlutils.copy import copy

    rb = xlrd.open_workbook("0815patent.xlsx")

    # 通过sheet_by_index()获取的sheet没有write()方法
    rs = rb.sheet_by_index(1)
    wb = copy(rb)

    # 通过get_sheet()获取的sheet有write()方法
    ws = wb.get_sheet(1)
    count = tag_row
    i = 0
    for data in resArray:
        ws.write(count,3+i,data)
        i = i+1
    wb.save('0815patent.xlsx')


def action():
    array = readExcel()
    # resRes = []
    tag_row = 1
    count = 0
    for cyear,cname in array:
        if count == 0:
            print "采集数据位置:",cname
            tag_row = cname
            count += 1
        else:
            cintYear = int(cyear)
            f5y = cintYear - 5
            f1y = cintYear - 1
            z0y = cintYear
            z1y = cintYear + 1
            z2y = cintYear + 2

            d1 = postValue(cname, appendYearString(f5y)[0], appendYearString(f5y)[1])
            time.sleep(1)
            d2 = postValue(cname, appendYearString(f1y)[0], appendYearString(f1y)[1])
            time.sleep(1)
            d3 = postValue(cname, appendYearString(z0y)[0], appendYearString(z0y)[1])
            time.sleep(1)
            d4 = postValue(cname, appendYearString(z1y)[0], appendYearString(z1y)[1])
            time.sleep(1)
            d5 = postValue(cname, appendYearString(z2y)[0], appendYearString(z2y)[1])
            time.sleep(1)

            print "正在放入缓存list"
            writeExcel([d1,d2,d3,d4,d5],tag_row)
            tag_row += 1
            count += 1
            print ''

    print "已经结束"


def appendYearString(year):
    start = str(year)+".01.01"
    end = str(year)+".12.31"
    return [start,end]

if __name__ == "__main__":
    action()