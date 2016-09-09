# -*- coding:utf-8 -*-
import urllib2  
import urllib
import sys 
import gzip
import chardet
from bs4 import BeautifulSoup
from StringIO import StringIO
reload(sys) 
sys.setdefaultencoding('utf8') 


soup = BeautifulSoup(open("test.html"))
# print type((soup.select(".patent"))[1])
group = soup.select(".patent")
count = soup.select("input #result_totalCount")
print "总计专利数:",count[0].get("value")
for gr in group:
	data = (gr.select("td"))
	data1 = data[2].string.strip()
	data2 = data[4].string.strip()

	number = (gr.select("span"))
	number1 = number[0].string
	number2 = number[1].string
	content = number[2].string

	print 'data1 :',data1
	print 'data2 :',data2
	print 'number1 :',number1
	print 'number2 :',number2
	print 'content :',content

	print ''