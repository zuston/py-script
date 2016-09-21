import sys
import time
import os
sys.path.append("..")
from bs4 import BeautifulSoup

from tool.Http import *

# http = Http()
# [code,msg,res] = http.open('http://www.zhihu.com/people/sha-cha-57',
#                     Cookie = 'd_c0="AEAAHF7tUgqPTser6aQFFNucOrpy_pVS_nM=|1470143843"; _zap=e0aa3eeb-4a2f-469a-b0c0-213999c8fad8; q_c1=9b67681f980240caad14cf09153f8cf4|1472825844000|1470143841000; l_cap_id="MjAyZjk4OWRkNWViNDg3NDk0Y2EzZDY3Y2RjNzMwN2Q=|1473305517|5e44a389c8a8d1c492f8e28b6c33558684f9709b"; cap_id="NWVjNTlmODg0ZjA0NDNjNmFjZjczYzVkOGE1NDVlOWM=|1473305517|483c89cfd8b6a38c9dfa3e64ca36874c5b1fc7f6"; login="ZWVhYzM3MDk5ZjMzNDdjOTlhYzc2OThiMzM1M2E2Yzg=|1473305538|b24862947894611df60da385d5321c7152828405"; __utmt=1; __utma=51854390.1478424689.1473601532.1474426191.1474436825.11; __utmb=51854390.3.9.1474436838115; __utmc=51854390; __utmz=51854390.1474436825.11.11.utmcsr=baidu.com|utmccn=(referral)|utmcmd=referral|utmcct=/index.php; __utmv=51854390.100-1|2=registration_date=20131021=1^3=entry_date=20131021=1; a_t="2.0AAAAmHsfAAAXAAAA5KsJWAAAAJh7HwAAAEAAHF7tUgoXAAAAYQJVTcJo-FcAPd0Msxz2C-lOeeikr99GzbSowiV5bg9W3imFV1LlbeAWXvSVBCxarA=="; z_c0=Mi4wQUFBQW1Ic2ZBQUFBUUFBY1h1MVNDaGNBQUFCaEFsVk53bWo0VndBOTNReXpIUFlMNlU1NTZLU3YzMGJOdEtqQ0pR|1474436836|6bf62efd8b544ab5415eda5bd7a08201827a15ac')
#
# if code==200:
#     print 'net connection is ok'
#     f = open('a.html','w')
#     f.write(res)



# soup = BeautifulSoup(open('a.html'),'lxml')


http = Http()
[code,msg,res] = http.open('http://bt0.com/film_31112.html')

if code == 200:
    print 'connection is ok'
    f = open('b.html','w')
    f.write(res)
    f.close()
