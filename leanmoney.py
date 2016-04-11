#coding:utf-8
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
import leancloud
from leancloud import Object
from leancloud import Query

#import tushare as ts
from pandas.compat import StringIO




class StockMoneyData(Object):	
	pass


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


def checkTingPai(stockCode):
	crawlHeader = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'}	
	url = "http://xueqiu.com/s/"+stockCode
	repeated = 1
	res = 0
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
			req.add_header("Host","xueqiu.com")			
			resp = urllib2.urlopen(req)			
			d = resp.read()
			if d.find("<div class=\"stock-closed\">")>-1:
				res = 1
			else:
				res = 0			
			repeated = 0			
		except Exception, e:
			print "find stock stop info exception, will download again after 5 seconds:", stockCode,str(e)
			time.sleep(2)
	return res


def downYesterdayTrade(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'.csv')==False:
		print "not find csv",stockCode
		return
	stock_data = pandas.read_csv(stockCode+'.csv')
	co = stock_data['date'].count()
	day = stock_data['date'][co-2]
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
			d = resp.read().decode('GBK')		
			df = pandas.read_table(StringIO(d), names=['time', 'price', 'change', 'volume', 'amount', 'type'], skiprows=[0]) 
			df.to_csv(tfile)	
			repeated = 0			
		except Exception, e:
			print "down history exception, will download again after 5 seconds:", stockCode,str(e)
			time.sleep(2)


def downTodayTrade(stockCode):
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
						time.sleep(2)			
			repeated = 0	
			f2.close()		
		except Exception, e:
			print "meet exception, will download again after 5 seconds:", str(e)
			time.sleep(2)


def calcTodayHighToLow(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'.csv')==False:
		print "not find csv",stockCode
		return (0,0,0)
	stock_data = pandas.read_csv(stockCode+'.csv')
	co = stock_data['date'].count()
	thigh = stock_data['high'][co-1]
	tlow = stock_data['low'][co-1]
	t = stock_data['date'][co-1]
	avp = numpy.round((thigh+tlow)*0.5,2)
	if os.path.exists(pa+'/'+stockCode+"_"+t+"_trade.csv")==False:
		print "not find trade csv",stockCode
		return (0,0,0)
	stock1 = pandas.read_csv(stockCode+"_"+t+"_trade.csv")

	prices = []
	for x in stock1['price']:
		prices.append(x)

	s = set(prices)

	bigsum = 0
	bigamount = 0
	smallsum = 0
	smallamount = 0
	avb = 0
	avs = 0
	rate = 0
	for x in s:
		z = 0
		for y in stock1['price']:
			tt = stock1['volume'][z]		
			am = stock1['amount'][z]
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
	if smallsum!=0:
		rate = numpy.round(float(bigsum)/float(smallsum),2)
	return (rate,avb,avs)


def calcYesterdayHighToLow(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'.csv')==False:
		print "not find csv",stockCode
		return (0,0,0)
	stock_data = pandas.read_csv(stockCode+'.csv')
	co = stock_data['date'].count()
	thigh = stock_data['high'][co-2]
	tlow = stock_data['low'][co-2]
	t = stock_data['date'][co-2]
	avp = numpy.round((thigh+tlow)*0.5,2)
	if os.path.exists(pa+'/'+stockCode+"_"+t+"_trade.csv")==False:
		print "not find trade csv",stockCode
		return (0,0,0)
	stock1 = pandas.read_csv(stockCode+"_"+t+"_trade.csv")

	prices = []
	for x in stock1['price']:
		prices.append(x)

	s = set(prices)

	bigsum = 0
	bigamount = 0
	smallsum = 0
	smallamount = 0
	avb = 0
	avs = 0
	rate = 0
	for x in s:
		z = 0
		for y in stock1['price']:
			tt = stock1['volume'][z]		
			am = stock1['amount'][z]
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
	if smallsum!=0:
		rate = numpy.round(float(bigsum)/float(smallsum),2)
	return (rate,avb,avs)


#down yesterday trade xls
#down today trade to csv
#calc yesterday high,low info
#calc today high,low info
#save to leancloud
'''
scod = "sz000838"

tp = checkTingPai(scod)
if tp==0:
	downYesterdayTrade(scod)
	downTodayTrade(scod)
	yrate,yhigh,ylow = calcYesterdayHighToLow(scod)
	trate,thigh,tlow = calcTodayHighToLow(scod)
	print yrate,yhigh,ylow,trate,thigh,tlow
'''


f = codecs.open('allstdata3.json','r',encoding='utf-8')
sss = json.loads(f.read())
f.close()	

leancloud.init('qazb7phh0uxqarjyd0agnbw7qwu65xff0e98sbbejfx8wyat', master_key='awfwb8rjhozpmmilpf7r339jx3qcjyuai7nqkk1qwfbnhu9x')

for x in sss:
	print "process:",x['stcode']
	tp = checkTingPai(x['stcode'])
	if tp==0:
		downYesterdayTrade(x['stcode'])
		downTodayTrade(x['stcode'])
		yrate,yhigh,ylow = calcYesterdayHighToLow(x['stcode'])
		trate,thigh,tlow = calcTodayHighToLow(x['stcode'])
		item = StockMoneyData()
		item.set('stcode',x['stcode'])
		item.set('yesterdayRate',yrate)
		item.set('yesterdayHighAvg',yhigh)
		item.set('yesterdayLowAvg',ylow)
		item.set('todaydayRate',trate)
		item.set('todayHighAvg',thigh)
		item.set('todayLowAvg',tlow)
		repeated = 1
		while repeated:
			try:
				item.save()
				repeated=0
			except Exception, e:
				print "exception on save :",x['stcode'],e
				time.sleep(2)


