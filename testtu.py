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
import re
socket.setdefaulttimeout(10.0) 
from bson import BSON
from bson import json_util
from datetime import datetime, timedelta
import matplotlib.pyplot as plt  
import matplotlib.patches as patches

import tushare as ts
from pandas.compat import StringIO


class StockTicker(HTMLParser):
	def __init__(self,df):
		HTMLParser.__init__(self)
		self.datas = df		
		self.findtable = 0
		self.findtbody = 0
		self.indata = 0
		self.inthtd = 0
		
		self.val = ""


	def handle_starttag(self, tag, attrs):
		if tag=='table':
			for x in attrs:				
				if (x[0]=='class') and (x[1]=='datatbl'):
					self.findtable = 1
		if (tag=='tbody') and (self.findtable==1):
			self.findtbody=1
		if (tag=='tr') and (self.findtbody==1):
			self.indata = 1
			self.val = ""
		if (tag=='th') and (self.indata==1):
			self.inthtd = 1
		if (tag=='td') and (self.indata==1):
			self.inthtd = 1
			

	def handle_endtag(self, tag):
		if tag=='table':
			self.findtable = 0
		if tag=='tbody':
			self.findtbody = 0
		if (tag=='tr') and (self.indata==1):
			self.indata = 0
			self.val += '\n'
			self.datas.write(self.val)
			self.val = ""
		if tag=='th':
			self.inthtd = 0
		if tag=='td':
			self.inthtd = 0
		

	def handle_data(self, data):
		if self.inthtd==1:
			s = data			
			s = s.replace('<h1>','')
			s = s.replace('<h5>','')
			s = s.replace('<h6>','')
			s = s.replace('</h1>','')
			s = s.replace('</h5>','')
			s = s.replace('</h6>','')
			s = s.replace(',','')
			s += ','
			self.val += s			


def getweekmacdcha(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_weekewma.csv')==False:
		print stockCode," week data not exists"
		return
	stock_data = pandas.read_csv(stockCode+'_weekewma.csv')
	co = stock_data['close'].count()
	if co<=30:
		return 0
	sco = stock_data['DEA'].count()
	yesterdayk = stock_data['DIFF'][co-2]
	k = stock_data['DIFF'][co-1]
	yesterdayd = stock_data['DEA'][co-2]
	d = stock_data['DEA'][co-1]
	v1 = yesterdayk - yesterdayd
	v2 = k - d
	if (v1<0) and (v2<0) and (v2>v1) and (v2>-0.15) and (v2*2<v1):
		return 1
	else:
		return 0

def getnewstlist():	
	f = codecs.open('allstdata3.json','r',encoding='utf-8')
	sss = json.loads(f.read())
	f.close()
	return sss	

stcode = 'sz300037'
day = "2016-03-04"

avpri = (37.89+35.36)*0.5
stock_data = pandas.read_csv(stcode+"_"+day+"_trade.csv")

bigsum = 0
smallsum = 0
k = 0
for x in stock_data['price']:
	v = stock_data['volume'][k]
	if (x>avpri) and (v>=100) :
		bigsum += v
	elif (x<avpri) and (v>=100):
		smallsum += v
	else:
		k +=1
		continue
	k += 1

print "big buyer:",bigsum
print "small buyer:",smallsum


'''
stlists = getnewstlist()


for x in stlists:
	j = getweekmacdcha(x['stcode'])
	if j==1:
		print x['stcode']
'''

'''
stock_data = pandas.read_csv('sz300262-trade.csv')
co = stock_data['volume'].count()
print co
i = 0
buy = 0
sumbuy = 0
sell = 0
sumsell = 0
for x in stock_data['volume']:
	#print stock_data['type'][i].decode('utf-8')
	v = stock_data['type'][i]
	v = v.decode('utf-8')
	if (v==u"买盘") and (x>=100):
		#big buy
		buy += x
		sumbuy += stock_data['amount'][i]
	if (v==u"卖盘") and (x>=100):
		sell += x
		sumsell += stock_data['amount'][i]
	
	i += 1
avgpr1 = sumbuy/(buy*100)
avgpr2 = sumsell/(sell*100)

print "buy :", buy , " total: ",sumbuy , " avg price: ",avgpr1
print "sell:", sell, " total: ",sumsell, " avg price: ",avgpr2
'''

'''
crawlHeader = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'}	
url = "http://market.finance.sina.com.cn/downxls.php?date=2016-02-15&symbol=sz000019"
realtimeurl = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Transactions.getAllPageTime?date=2016-02-26&symbol=sz300262"
pageurl = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol=sz300262&date=2016-02-26&page="
repeated = 1
while repeated:		
	try:
		cookie = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		urllib2.install_opener(opener)
		req = urllib2.Request(realtimeurl,None,crawlHeader)
		req.add_header("Accept","*/*")
		req.add_header("Accept-Language", "*")
		req.add_header("Connection", "keep-alive")
		req.add_header("Accept-Encoding", "none")
		req.add_header("X-Requested-With", "XMLHttpRequest")
		req.add_header("Referer", "http://baidu.com")
		req.add_header("Cache-Control","no-cache")
		req.add_header("X-Requested-With","XMLHttpRequest")
		req.add_header("Host","vip.stock.finance.sina.com.cn")			
		resp = urllib2.urlopen(req)
		#print resp.getcode()
		#d = resp.read().decode('GBK')		
		#df = pandas.read_table(StringIO(d), names=['time', 'price', 'change', 'volume', 'amount', 'type'], skiprows=[0]) 
		#df.to_csv('sz000019_tick.csv')		
		d = resp.read().decode('GBK')
		
		ar = d.split("{page:")
		
		i = len(ar)
		s = ar[i-1]
		
		idx = s.find(',')
		
		lastpage = s[:idx]
		
		ci = int(lastpage)
		f2 = codecs.open('sz300262-trade.csv','w',encoding='utf-8')
		f2.write("time,price,percent,change,volume,amount,type,\n")
		for x in range(1,ci+1):
			repeated2 = 1
			while repeated2:
				try:
					pu = pageurl+str(x)
					req2 = urllib2.Request(pu,None,crawlHeader)
					req2.add_header("Accept","*/*")
					req2.add_header("Accept-Language", "*")
					req2.add_header("Connection", "keep-alive")
					req2.add_header("Accept-Encoding", "none")
					req2.add_header("X-Requested-With", "XMLHttpRequest")
					req2.add_header("Referer", "http://baidu.com")
					req2.add_header("Cache-Control","no-cache")
					req2.add_header("X-Requested-With","XMLHttpRequest")
					req2.add_header("Host","vip.stock.finance.sina.com.cn")			
					resp2 = urllib2.urlopen(req2)
					d2 = resp2.read().decode('GBK')
					ana = StockTicker(f2)
					ana.feed(d2)
					repeated2 = 0
				except Exception, e2:
					print "parse ticker error:,",str(e2)
					time.sleep(5)
			

		repeated = 0	
		f2.close()		
	except Exception, e:
		print "meet exception, will download again after 5 seconds:", str(e)
		time.sleep(5)

'''


#df = ts.get_tick_data('300187',date='2016-02-25')
#print df
#df = ts.get_today_ticks('000019')
#print df
