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


def getHistoryRecord(stockCode,day):
	histurl = "http://market.finance.sina.com.cn/downxls.php?date="+day+"&symbol="+stockCode
	tfile = stockCode+"_"+day+"_trade.csv"
	crawlHeader = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'}	
	repeated = 1
	while repeated:		
		try:
			cookie = cookielib.CookieJar()
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
			urllib2.install_opener(opener)
			req = urllib2.Request(histurl,None,crawlHeader)
			req.add_header("Accept","*/*")
			req.add_header("Accept-Language", "*")
			req.add_header("Connection", "keep-alive")
			req.add_header("Accept-Encoding", "none")
			req.add_header("X-Requested-With", "XMLHttpRequest")
			req.add_header("Referer", "http://baidu.com")
			req.add_header("Cache-Control","no-cache")
			req.add_header("X-Requested-With","XMLHttpRequest")
			req.add_header("Host","market.finance.sina.com.cn")			
			resp = urllib2.urlopen(req)
			#print resp.getcode()
			d = resp.read().decode('GBK')		
			df = pandas.read_table(StringIO(d), names=['time', 'price', 'change', 'volume', 'amount', 'type'], skiprows=[0]) 
			df.to_csv(tfile)	
			repeated = 0			
		except Exception, e:
			print "down history exception, will download again after 5 seconds:", stockCode,str(e)
			time.sleep(5)

def getTodayRecord(stockCode):
	tday = time.strftime('%Y-%m-%d',time.localtime())
	tfile = stockCode+"_"+tday+"_trade.csv"
	realtimeurl = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Transactions.getAllPageTime?date="+tday+"&symbol="+stockCode
	pageurl = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol="+stockCode+"&date="+tday+"&page="
	crawlHeader = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'}	
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
			d = resp.read().decode('GBK')		
			ar = d.split("{page:")		
			i = len(ar)
			s = ar[i-1]		
			idx = s.find(',')		
			lastpage = s[:idx]		
			ci = int(lastpage)
			f2 = codecs.open(tfile,'w',encoding='utf-8')
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


def getTradeRecord(stockCode):
	#get trading days
	tradingDays = []
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'.csv')
	co = stock_data['close'].count()
	for x in xrange(co-16,co-1):
		tradingDays.append(stock_data['date'][x])
	for x in tradingDays:
		getHistoryRecord(stockCode,x)

	getTodayRecord(stockCode)



def analyseStock(stockCode,day):
	per = 0
	if os.path.exists(stockCode+'_ewma.csv')==True:
		szdata = pandas.read_csv(stockCode+"_ewma.csv")
		cc = szdata['close'].count()
		start = 0
		fd = 0
		for d in szdata['date']:
			if d==day:
				fd = start
				break
			start += 1
		if fd!=0:
			per = szdata['percent'][fd]
	tfile = stockCode+"_"+day+"_trade.csv"
	stock_data = pandas.read_csv(tfile)
	co = stock_data['volume'].count()
	i = 0
	allbuy = 0
	allbuysum = 0
	allsell = 0
	allsellsum = 0
	buy = 0
	sumbuy = 0
	sell = 0
	sumsell = 0
	prebuyprice = 0
	presellprice = 0
	for x in stock_data['volume']:
		#print stock_data['type'][i].decode('utf-8')
		v = stock_data['type'][i]
		v = v.decode('utf-8')
		if (v==u"买盘") and (x>=100):
			#big buy
			buy += x
			sumbuy += stock_data['amount'][i]
		if (v==u"买盘"):
			allbuy += x			
			allbuysum += stock_data['amount'][i] 
		if (v==u"卖盘") and (x>=100):
			sell += x
			sumsell += stock_data['amount'][i]		
		if (v==u"卖盘"):
			allsell += x
			allsellsum += stock_data['amount'][i]		
	
		i += 1
	avgpr1 = 0
	if buy!=0:
		avgpr1 = numpy.round(float(sumbuy)/(buy*100),2)
	avgpr2 = 0
	if sell!=0:
		avgpr2 = numpy.round(float(sumsell)/(sell*100),2)

	print "***************",stockCode,"*****",day,"****************",per
	print "big buy count: ", buy , " total amount: ",sumbuy , " buy average: ",avgpr1
	print "big sell count: ", sell, " total amount: ",sumsell, " sell average: ",avgpr2
	print "all buy: ", allbuy , " all buy amount: ",allbuysum
	print "all sell: ", allsell, " all sell amount: ",allsellsum
	print "big buy- big sell:",sumbuy-sumsell
	print "all buy - all sell: ", allbuysum - allsellsum
	print "\n"

def testtotal(stockCode,day):
	tfile = stockCode+"_"+day+"_trade.csv"
	stock_data = pandas.read_csv(tfile)
	t = 0
	for x in stock_data['volume']:
		t += x
	print "total:",t
		

def analyseZhuLiStock(stockCode,day):
	tfile = stockCode+"_"+day+"_trade.csv"
	stock_data = pandas.read_csv(tfile)
	co = stock_data['volume'].count()
	
	prebuyprice = 0
	presellprice = 0
	lstime = 0
	pstime = 0
	lz = range(1,co-1)
	lz.reverse()
	print "***************",day,"****************"
	for x in lz:
		v = stock_data['type'][x]
		v = v.decode('utf-8')
		vo = stock_data['volume'][x]
		if (v==u"买盘") and (prebuyprice==0):
			prebuyprice = stock_data['price'][x]
		else:
			if (v==u"买盘") and (vo>100) and (prebuyprice!=0):
				p = stock_data['price'][x]
				per = (p-prebuyprice)/prebuyprice*100
				if (per>0.3):
					print "up ",stock_data['time'][x]," price: ",stock_data['price'][x], " count: ",vo
					lstime += 1
				prebuyprice = p
			else:
				prebuyprice = stock_data['price'][x]				

		if (v==u"卖盘") and (presellprice==0):
			presellprice = stock_data['price'][x]
		else:
			if (v==u"卖盘") and (vo>100) and (presellprice!=0):
				p = stock_data['price'][x]
				per = (presellprice-p)/p*100
				if (per>0.3):
					print "down ",stock_data['time'][x]," price: ",stock_data['price'][x]," count: ",vo
					pstime += 1
				presellprice = p
			else:
				presellprice = stock_data['price'][x]
	print "up time:",lstime
	print "down time:",pstime
	print "\n"



def getHighLow(stockCode):
	crawlHeader = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'}	
	url= "http://qt.gtimg.cn/q="+stockCode
	repeated = 1
	tdopen = 0
	tdhigh = 0
	tdlow = 0
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
			tdhigh=float(arr[33])
			tdlow=float(arr[34])
			repeated = 0			
		except Exception, e:
			print "down hq sina exception, will download again after 5 seconds:", stockCode,str(e)
			time.sleep(2)
	return (tdhigh,tdlow)


def analyseHighLowExchange(stcode):
	t = time.strftime('%Y-%m-%d',time.localtime())
	th,tl = getHighLow(stcode)

	avp = (th+tl)*0.5

	stock_data = pandas.read_csv(stcode+"_"+t+"_trade.csv")

	print "*************",stcode,"****",t,"***************"

	prices = []
	for x in stock_data['price']:
		prices.append(x)

	s = set(prices)

	bigsum = 0
	bigamount = 0
	smallsum = 0
	smallamount = 0
	avs = 0
	avb = 0
	for x in s:
		z = 0
		for y in stock_data['price']:
			tt = stock_data['volume'][z]		
			am = stock_data['amount'][z]
			if (y>avp) and (tt>100):
				bigsum += tt
				bigamount += am
			elif (y<avp) and (tt>100):
				smallsum += tt
				smallamount += am
			else:
				z += 1
				continue
			z += 1
	if bigsum!=0:
		avb = numpy.round(float(bigamount)/float(bigsum*100),2)
	if smallsum!=0:
		avs = numpy.round(float(smallamount)/float(smallsum*100),2)
	print "big:",bigsum," average price:",avb
	print "small:",smallsum," average price:",avs
	print "big-small:",bigsum-smallsum
	if (bigsum-smallsum)>0:
		print u"高位换手, 逃"
	else:
		print u"低位换手, 抄"
	print "\n"

#getHistoryRecord("sz002416","2016-02-23")
#getHistoryRecord("sz002416","2016-02-24")
#getHistoryRecord("sz002416","2016-02-25")
#getHistoryRecord("sz002416","2016-02-26")
#getHistoryRecord("sz002416","2016-02-29")
#getHistoryRecord("sz002416","2016-03-01")
#getTodayRecord("sz002416")
#getTradeRecord("sh600283")

#analyseZhuLiStock("sz300187","2016-02-29")

#testtotal("sz002416","2016-02-29")


#analyseStock("sz002416","2016-02-23")
#analyseStock("sz002416","2016-02-24")
#analyseStock("sz002416","2016-02-25")
#analyseStock("sz002416","2016-02-26")
#analyseStock("sz002416","2016-02-29")
#analyseStock("sz002416","2016-03-01")
#analyseStock("sh600283","2016-03-02")

st = sys.argv[1]
#st = "sh603300"

days = []
stock_data = pandas.read_csv(st+'.csv')
co = stock_data['close'].count()
z = range(co-15,co)
for t in z:
	days.append(stock_data['date'][t])
lastday = stock_data['date'][co-1]
for y in days:
	getHistoryRecord(st,y)
getTodayRecord(st)
#for y in days:
	#analyseStock(st,y)
	#analyseZhuLiStock(st,y)
tday = time.strftime('%Y-%m-%d',time.localtime())
analyseStock(st,tday)
analyseZhuLiStock(st,tday)
analyseHighLowExchange(st)


#show picture
sd = pandas.read_csv(st+'_'+tday+'_trade.csv')

i=0

yy = []
zz = []
bb = []
dd = []
for x in sd['volume']:
	if x>=1000:
		yy.append(x)		
		zz.append(sd['price'][i])
		bb.append(sd['type'][i])
		dd.append(sd['time'][i])
	i += 1

dd.reverse()
yy.reverse()
zz.reverse()
bb.reverse()

day1 = stock_data['date'][co-1]
sd1 = pandas.read_csv(st+'_'+day1+'_trade.csv')

i=0

yy1 = []
zz1 = []
bb1 = []
dd1 = []
for x in sd1['volume']:
	if x>=1000:
		yy1.append(x)		
		zz1.append(sd1['price'][i])
		bb1.append(sd1['type'][i])
		dd1.append(sd1['time'][i])
	i += 1

dd1.reverse()
yy1.reverse()
zz1.reverse()
bb1.reverse()

day2 = stock_data['date'][co-2]
sd2 = pandas.read_csv(st+'_'+day2+'_trade.csv')

i=0

yy2 = []
zz2 = []
bb2 = []
dd2 = []
for x in sd2['volume']:
	if x>=1000:
		yy2.append(x)		
		zz2.append(sd2['price'][i])
		bb2.append(sd2['type'][i])
		dd2.append(sd2['time'][i])
	i += 1

dd2.reverse()
yy2.reverse()
zz2.reverse()
bb2.reverse()

for t in yy1:
	yy2.append(t)
for t in yy:
	yy2.append(t)

for t in zz1:
	zz2.append(t)
for t in zz:
	zz2.append(t)

for t in dd1:
	dd2.append(t)
for t in dd:
	dd2.append(t)

for t in bb1:
	bb2.append(t)
for t in bb:
	bb2.append(t)





co = len(yy2)
xx = range(0,co)

#plt.scatter(xx,yy)
xbar = plt.bar(xx,yy2,0.5,color='r',picker=True)

i = 0
buysum = 0
buycount = 0
sellsum = 0
sellcount = 0
for b in xbar:
	if bb2[i].decode('utf-8')==u"买盘":
		xbar[i].set_color('r')
		buysum += yy2[i]*zz2[i]
		buycount += yy2[i]
	elif bb2[i].decode('utf-8')==u"卖盘":
		xbar[i].set_color('g')
		sellsum += yy2[i]*zz2[i]
		sellcount += yy2[i]
	else:
		xbar[i].set_color('y')
	i += 1

print "buy count:",buycount
print "buy average price:",numpy.round(buysum/buycount,2)
print "sell count:",sellcount
print "sell average price:",numpy.round(sellsum/sellcount,2)


plt.title(st+" "+tday)
plt.xlabel("time")
plt.ylabel("Volume")

i = 0
for x in zz2:
	h = xbar[i].get_height() + 10
	x1 = xbar[i].get_x()
	plt.text(x1,h,str(zz2[i]))
	#plt.text(x1,h+80,str(dd2[i]))
	i += 1


#plt.xticks([w*7*24 for w in range(10)],['week %i'%w for w in range(10)])
plt.autoscale(tight=True)
plt.grid()
plt.show()





'''
#get kdj,back / macd,back / weekmacd , high / yaogu from local json file
slist=[]
f = codecs.open('shdata.json','r',encoding='utf-8')
shdatas = json.loads(f.read())
for x in shdatas:
	#kdj, kdjback
	if (x['kdj']>0) and (x['kdjback']==1):
		slist.append(x['stcode'])
	#macd, macdback
	if (x['macd']>0) and (x['macdback']==1):
		slist.append(x['stcode'])
	#week
	if (x['weekmacd']>0) and (x['weekhighmacd']==1):
		slist.append(x['stcode'])
	#yaogu
	if (x['fourdayfluck']>=35) and (x['weekhighmacd']==1):
		slist.append(x['stcode'])
f.close()

f = codecs.open('szdata.json','r',encoding='utf-8')
szdatas = json.loads(f.read())
for x in szdatas:
	#kdj, kdjback
	if (x['kdj']>0) and (x['kdjback']==1):
		slist.append(x['stcode'])
	#macd, macdback
	if (x['macd']>0) and (x['macdback']==1):
		slist.append(x['stcode'])
	#week
	if (x['weekmacd']>0) and (x['weekhighmacd']==1):
		slist.append(x['stcode'])
	#yaogu
	if (x['fourdayfluck']>=35) and (x['weekhighmacd']==1):
		slist.append(x['stcode'])
f.close()

f = codecs.open('cydata.json','r',encoding='utf-8')
cydatas = json.loads(f.read())
for x in cydatas:
	#kdj, kdjback
	if (x['kdj']>0) and (x['kdjback']==1):
		slist.append(x['stcode'])
	#macd, macdback
	if (x['macd']>0) and (x['macdback']==1):
		slist.append(x['stcode'])
	#week
	if (x['weekmacd']>0) and (x['weekhighmacd']==1):
		slist.append(x['stcode'])
	#yaogu
	if (x['fourdayfluck']>=35) and (x['weekhighmacd']==1):
		slist.append(x['stcode'])
f.close()


#get 15 days trading record
for x in slist:
	days = []
	stock_data = pandas.read_csv(x+'.csv')
	co = stock_data['close'].count()
	days.append(stock_data['date'][co-6])
	days.append(stock_data['date'][co-5])
	days.append(stock_data['date'][co-4])
	days.append(stock_data['date'][co-3])
	days.append(stock_data['date'][co-2])
	lastday = stock_data['date'][co-1]
	for y in days:
		getHistoryRecord(x,y)
	getTodayRecord(x)
	for y in days:
		analyseStock(x,y)
	analyseStock(x,lastday)
'''

