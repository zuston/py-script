# -*- coding:utf-8 -*-
import urllib2  
import urllib
import sys 
import gzip
from StringIO import StringIO
from bs4 import BeautifulSoup
reload(sys) 
sys.setdefaultencoding('utf8') 
# print sys.getdefaultencoding()

url = 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showSearchResult-startWa.shtml'
# url = 'http://www.baidu.com'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'  
values = {	
			'resultPagination.limit' : 1000,  
			'resultPagination.sumLimit' : 10,
			'resultPagination.start' : 1,
			'resultPagination.totalCount' : 10984,
			'resultQC.executableSearchExp' : '',
			'searchCondition.searchType' : 'Sino_foreign',
			'searchCondition.resultMode' : 'TABLE_MODE',
			'searchCondition.searchKeywords_str' : '@@[上][ ]{0,}[海][ ]{0,}[大][ ]{0,}[学][ ]{0,}@@',
			'searchCondition.literatureSF' : '复合申请人与发明人=(上海大学)',
			# 'resultQC.literaExecutableSearchExp' : '',
			# 'searchCondition.strategy' : '',
			# 'resultQC.dataExecutableSearchExp' : '',
			# 'searchCondition.literatureSF' : '',
			# 'searchCondition.ssId' : '',
			'searchCondition.sortFields' : '-APD,+PD',
			# 'resultQC.displayFields' : '',
			'searchCondition.searchExp' : '复合申请人与发明人=(上海大学)',
			# 'searchCondition.displayFields' : '',
			'searchCondition.executableSearchExp' : "VDB:(IBI='上海大学')",
			'wee.bizlog.modulelevel' : '0200602',
			# 'searchCondition.dbId' : '',
			'searchCondition.searchKeywords' : '[上][ ]{0,}[海][ ]{0,}[大][ ]{0,}[学][ ]{0,}',
		}

# resultPagination.limit	12
# resultPagination.sumLimit	10
# resultPagination.start	12
# resultPagination.totalCount	10984
# resultQC.executableSearchExp	
# searchCondition.searchType	Sino_foreign
# searchCondition.resultMode	TABLE_MODE
# searchCondition.searchKeywords_str	@@[上][ ]{0,}[海][ ]{0,}[大][ ]{0,}[学][ ]{0,}@@
# resultQC.literaExecutableSearchExp	
# searchCondition.strategy	
# resultQC.dataExecutableSearchExp	
# searchCondition.literatureSF	
# searchCondition.ssId	
# searchCondition.sortFields	-APD,+PD 
# resultQC.displayFields	
# searchCondition.searchExp	复合申请人与发明人=(上海大学)
# searchCondition.displayFields	
# searchCondition.executableSearchExp	VDB:(IBI='上海大学')
# wee.bizlog.modulelevel	0200602
# searchCondition.dbId	
# searchCondition.searchKeywords	
# searchCondition.searchKeywords	[上][ ]{0,}[海][ ]{0,}[大][ ]{0,}[学][ ]{0,}

headers = { 'User-Agent' : user_agent }  
data = urllib.urlencode(values)

# proxy_handler = urllib2.ProxyHandler({"http" : '114.27.130.240:3128'})
# opener = urllib2.build_opener(proxy_handler)
# urllib2.install_opener(opener) 

request = urllib2.Request(url,data,values)
# 暂停爬取，进行解析
try:
	response = urllib2.urlopen(request,timeout=100) 

	print response.info().get('Content-Encoding')
	# page = response.read()
	buf = StringIO(response.read())
	f = gzip.GzipFile(fileobj=buf)
	data = f.read()
	soup = BeautifulSoup(data)
	# print type((soup.select(".patent"))[1])
	group = soup.select(".patent")
	for gr in group:
		print gr.select("span")
		print ''
	print "总计条目数:",len(group)
except urllib2.URLError:
	print "超时"
