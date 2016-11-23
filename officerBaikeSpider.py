#!coding:utf-8

import sys
import time
import os
import xlrd
sys.path.append("..")
from bs4 import BeautifulSoup as bs
from pyTool.tool.Http import *
import xlwt


class base(object):
    def __init__(self):
        self.dataPath = './data/officerExcel/'

    def readData(self,fileName):
        dataSet = set()
        if os.path.exists(self.dataPath) and os.path.isfile(self.dataPath+fileName):
            excelName = self.dataPath+fileName
            tag_row = 1
            book = xlrd.open_workbook(excelName, encoding_override='utf-8')
            sh = book.sheet_by_index(0)

            for rx in range(tag_row,sh.nrows):
                province = str((sh.row(rx))[1].value)
                city = str(sh.row(rx)[3].value)
                area = str(sh.row(rx)[5].value)
                name = str(sh.row(rx)[7].value)
                # print province + ' ' + city + ' ' + area + ' ' + name
                if name!='N\A' or name!='' or name!=None:
                    dataSet.add(province.strip()+':'+city.strip()+area.strip()+':'+name.strip())
            return dataSet
        else:
            print 'file path error'
            return dataSet


class spider(object):
    def __init__(self,string):
        self.requestUrl = 'http://baike.baidu.com/search/word?word='
        self.http = Http()
        self.secondUrl = 'http://baike.baidu.com'
        self.searchWord(string)

    def searchWord(self,string):
        splitList = string.split(':')
        self.keyword = splitList[-1]
        self.limitWord = splitList[:-1]

    def start(self):
        code,msg,res = self.http.open(self.requestUrl+self.keyword)
        if code==200:
            self.analyze(res,self.limitWord)


    def analyze(self,res,limitWord):
        self.soup = bs(res,'html.parser')
        polysemant = self.soup.find('div',class_='polysemant-list polysemant-list-normal')
        if polysemant==None:
            tool.echo(self.keyword+' 无异议')
            return 0,self.parserData(res)
        else:
            max = [0,'']
            for line in polysemant.findAll('li'):
                content = line.text
                weight = 0
                for oneLimit in limitWord:
                    if oneLimit in content:
                        weight+=1
                if max[0]<weight:
                    max[0] = weight
                    max[1] = line
            if max[0]==0:
                tool.echo(self.keyword + '  未找到此人的关联信息')
                return -1,'error'

            info = max[1]
            if info.find('span',class_='selected')!=None:
                tool.echo(self.keyword + '  已选择：' + info.text)
                return 1,self.parserData(res)

            tool.echo(self.keyword + '  优先选择' + info.text)

            return 2, self.parserData(self.polysemantAchive(info.a['href']))



    def polysemantAchive(self,url):
        code,msg,res = self.http.open(self.secondUrl+url)
        if code==200:
            return res
        else:
            return ''

    def parserData(self,res):
        infomation = self.soup.findAll('div',class_='para')
        entity = bean()

        pass

    def instanceBean(self,list):
        self.bean = bean()
        return self.bean


class bean(object):
    def __init__(self):
        self.province = ''
        self.city = ''
        self.area = ''

        self.name = ''
        self.info = ''
        self.birth = ''
        self.nativePlace = ''
        self.nation = ''
        self.resume = ''


class tool(object):
    @staticmethod
    def echo(string,flag=1):
        if flag:
            print string


def test():
    soup = bs(open('./data/test.html'),'html.parser')
    polysemant = soup.find('div', class_='polysemant-list polysemant-list-normal')
    for line in polysemant.find_all('li'):
        if line.find('span', class_='selected') != None:
            continue
        print line.a['href']
        exit(1)



if __name__ == '__main__':
    b = base()
    for i in b.readData('县委书记名单.xls'):
        # i为若干限定词和一个关键词组成的string
        s = spider(i)
        s.start()