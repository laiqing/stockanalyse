#coding = utf-8
#!/usr/bin/python

import pymongo
import os,sys,json
import time
import urllib,urllib2
import httplib
import shutil
import linecache
import codecs
import cookielib
from HTMLParser import HTMLParser
import numpy
import pandas
from multiprocessing.dummy import Pool as ThreadPool
import socket
import math
import json
socket.setdefaulttimeout(10.0) 
import leancloud
from leancloud import Object
from leancloud import Query
import requests


'''
#u="/1.1/classes/CYStockData?where=%7B%22stcode%22%3A%22SZ300187%22%7D"
# /1.1/classes/CYStockData?where={"stcode":"SZ300187"}
#print urllib.unquote(u)


#crawlHeader = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'}	
crawlHeader = {'User-Agent':'curl/7.26.0'}
url = "https://api.leancloud.cn/1.1/classes/CYStockData"

con = {"where":{"stcode":"SZ300187"}}
#print urllib.quote(con)


req = urllib2.Request(url,None,crawlHeader)
req.add_header("Content-Type","application/json")
req.add_header("X-LC-Key","i1mhevfmnah0fpf5oqz09a5yun6cmjy90smj17j446tqs101")
req.add_header("X-LC-Id","qazb7phh0uxqarjyd0agnbw7qwu65xff0e98sbbejfx8wyat")

req.add_data(urllib.urlencode(con))

resp = urllib2.urlopen(req)


d = resp.read()
print d
'''

class SHStockData(Object):	
	pass

class SZStockData(Object):
	pass

class CYStockData(Object):
	pass

def getTodayVolume(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'.csv')
	co = stock_data['volume'].count()
	lastv = stock_data['volume'][co-1]
	#get sina code
	crawlHeader = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'}	
	#url = "http://hq.sinajs.cn/list="+stockCode
	url= "http://qt.gtimg.cn/q="+stockCode
	repeated = 1	
	while repeated:		
		try:
			cookie = cookielib.CookieJar()
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
			urllib2.install_opener(opener)
			req = urllib2.Request(url,None,crawlHeader)
			req.add_header("Accept","*/*")
			req.add_header("Accept-Language", "*")
			req.add_header("Connection", "keep-alive")
			req.add_header("Accept-Encoding", "none")
			req.add_header("X-Requested-With", "XMLHttpRequest")
			req.add_header("Referer", "http://baidu.com")
			req.add_header("Cache-Control","no-cache")
			req.add_header("X-Requested-With","XMLHttpRequest")
			req.add_header("Host","qt.gtimg.cn")			
			resp = urllib2.urlopen(req)			
			d = resp.read().decode('GBK')		
			if d.find("none_match")>-1:
				return 0
			fidx = d.find("\"")			
			eidx = d.find("\"",fidx+1)	
			s = d[fidx+1:eidx]
			arr = s.split('~')
			tdv=float(arr[6])			
			repeated = 0			
		except Exception, e:
			print "down hq sina exception, will download again after 5 seconds:", stockCode,str(e)
			time.sleep(2)
	if (tdv>=lastv*1.1):
		#greater , push notification
		return 1
	else:
		return 0


def getYesterdayKDJ(rlist):
	query = Query(CYStockData)  
	query.equal_to('kdjback', 1)
	query.greater_than('kdj',0)
	query.equal_to('volume',1)
	cyresults = query.find()
	for x in cyresults:
		rlist.append(x['stcode'])
	query = Query(SZStockData)  
	query.equal_to('kdjback', 1)
	query.greater_than('kdj',0)
	query.equal_to('volume',1)
	szresults = query.find()
	for x in szresults:
		rlist.append(x['stcode'])
	query = Query(SHStockData)  
	query.equal_to('kdjback', 1)
	query.greater_than('kdj',0)
	query.equal_to('volume',1)
	cyresults = query.find()
	for x in cyresults:
		rlist.append(x['stcode'])
	
	
def leanPush(ss):	
	url= "https://leancloud.cn/1.1/push"
	rdata = {}
	rdata["data"]={"alert":ss,"sound":"default"}
	rdata["prod"]="dev"
	header = {"X-LC-Id":"qazb7phh0uxqarjyd0agnbw7qwu65xff0e98sbbejfx8wyat","X-LC-Key":"i1mhevfmnah0fpf5oqz09a5yun6cmjy90smj17j446tqs101","Content-Type":"application/json"}
	d = requests.post(url,params=rdata,data=json.dumps(rdata),headers=header)
	print d



leancloud.init('qazb7phh0uxqarjyd0agnbw7qwu65xff0e98sbbejfx8wyat', master_key='awfwb8rjhozpmmilpf7r339jx3qcjyuai7nqkk1qwfbnhu9x')

rlist = []
getYesterdayKDJ(rlist)

print rlist

finals = []

for x in rlist:
	j = getTodayVolume(x)
	if j==1:
		finals.append(x)

s= ""
if len(finals)>0:
	s += u"今日量突破:"
	for x in finals:
		s += str(x)+";"
	s += u"建议关注!"


if s!="":
	leanPush(s)