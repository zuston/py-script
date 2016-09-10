# -*- coding:utf-8 -*-

import urllib
import urllib2
import sys
import gzip
from StringIO import StringIO
import time
from bs4 import BeautifulSoup as bs
reload(sys)
sys.setdefaultencoding("utf8")


def postValue(searchContent,startYear,endYear):
    print "正在装载数据"
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
    print "正在爬取"
    request = urllib2.Request(url, data, values)
    try:
        response = urllib2.urlopen(request, timeout=10)
        # print response.info().get('Content-Encoding')
        pageEncoding = response.info().get('Content-Encoding')
        resData = ''
        print "正在解析"
        if pageEncoding == 'gzip':
            buf = StringIO(response.read())
            f = gzip.GzipFile(fileobj=buf)
            resData = f.read()
        else:
            resData = response.read()

        soup = bs(resData)
        count = soup.select("input #result_totalCount")
        if count != []:
            print searchContent,"在",startYear,"到",endYear,"期间总计专利数:", count[0].get("value")
            return count[0].get("value")
        else:
            print searchContent,"未查到有关专利信息"
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
    for rx in range(1, sh.nrows):
        # print dir((sh.row(rx))[0])
        cid = str(((sh.row(rx))[0].value))
        cid = cid[:-2]
        cname = ((sh.row(rx))[2]).value
        array.append([cid,cname])
    # print array[0][1]
    # print array
    return array

def writeExcel(resArray):
    import xlrd
    from xlutils.copy import copy

    rb = xlrd.open_workbook("0815patent.xlsx")

    # 通过sheet_by_index()获取的sheet没有write()方法
    rs = rb.sheet_by_index(1)
    wb = copy(rb)

    # 通过get_sheet()获取的sheet有write()方法
    ws = wb.get_sheet(1)
    count = 1
    for d1,d2,d3,d4,d5 in resArray:
        ws.write(count,3,d1)
        ws.write(count,4,d2)
        ws.write(count,5,d3)
        ws.write(count,6,d4)
        ws.write(count,7,d5)
        count += 1
    wb.save('0815patent.xlsx')


def action():
    array = readExcel()
    resRes = []
    for cyear,cname in array:
        cintYear = int(cyear)
        f5y = cintYear-5
        f1y = cintYear-1
        z0y = cintYear
        z1y = cintYear+1
        z2y = cintYear+2

        d1 = postValue(cname,appendYearString(f5y)[0],appendYearString(f5y)[1])
        time.sleep(4)
        d2 = postValue(cname,appendYearString(f1y)[0],appendYearString(f1y)[1])
        time.sleep(6)
        d3 = postValue(cname,appendYearString(z0y)[0],appendYearString(z0y)[1])
        time.sleep(7)
        d4 = postValue(cname,appendYearString(z1y)[0],appendYearString(z1y)[1])
        time.sleep(2)
        d5 = postValue(cname,appendYearString(z2y)[0],appendYearString(z2y)[1])
        time.sleep(4)

        print "正在放入缓存list"
        resRes.append([d1,d2,d3,d4,d5])
        print ''
    writeExcel(resRes)

    print "已经结束"


def appendYearString(year):
    start = str(year)+".01.01"
    end = str(year)+".12.31"
    return [start,end]

if __name__ == "__main__":
    action()