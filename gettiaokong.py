#encoding:utf-8
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

from bson import BSON
from bson import json_util
from datetime import datetime, timedelta
import matplotlib.pyplot as plt  
import matplotlib.patches as patches

import tushare as ts
from pandas.compat import StringIO

def gettk(stockCode):
	print "process...",stockCode
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'.csv')
	co = stock_data['high'].count()
	lasth = stock_data['high'][co-1]
	#get sina code
	crawlHeader = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'}	
	#url = "http://hq.sinajs.cn/list="+stockCode
	url= "http://qt.gtimg.cn/q="+stockCode
	repeated = 1
	tdopen = 0
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
				break
			fidx = d.find("\"")			
			eidx = d.find("\"",fidx+1)	
			s = d[fidx+1:eidx]
			arr = s.split('~')
			tdopen=float(arr[5])
			repeated = 0			
		except Exception, e:
			print "down hq sina exception, will download again after 5 seconds:", stockCode,str(e)
			time.sleep(5)
	if (tdopen>=(lasth+0.3)):
		print "today chance: ",stockCode
		time.sleep(2)
		return 1
	else:
		time.sleep(2)
		return 0

def getLiang(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'.csv')
	stock_data['lowvolume89'] = pandas.rolling_min(stock_data['volume'],89)
	stock_data['lowvolume144'] = pandas.rolling_min(stock_data['volume'],144)
	stock_data['highvolume89'] = pandas.rolling_max(stock_data['volume'],89)
	stock_data['highvolume144'] = pandas.rolling_max(stock_data['volume'],144)
	co = stock_data['close'].count()
	if co<160:
		return 0
	lastv = stock_data['volume'][co-1]
	lastv2 = stock_data['volume'][co-2]
	ref2 = (lastv2 - stock_data['lowvolume89'][co-2])/(stock_data['highvolume89'][co-2] - stock_data['lowvolume89'][co-2])*100
	ref1 = (lastv - stock_data['lowvolume89'][co-1])/(stock_data['highvolume89'][co-1] - stock_data['lowvolume89'][co-1])*100
	if (ref2==0) and (ref1>0):
		return 1
	else:
		return 0














f = codecs.open('allstdata3.json','r',encoding='utf-8')
sss = json.loads(f.read())
f.close()	
mlist = []
for x in sss:
	mlist.append(x['stcode'])


#pool = ThreadPool(12)
#results = pool.map(gettk,mlist)
#pool.close()
#pool.join()



for x in mlist:
	#gettk(x)
	zzz = getLiang(x)
	if zzz==1:
		print x

