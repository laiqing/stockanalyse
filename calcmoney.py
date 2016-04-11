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

#import tushare as ts
from pandas.compat import StringIO


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


#th,tl=getHighLow("sz000019")	
#print th,tl


stcode = "sz002431"
stcode = sys.argv[1]


sd = pandas.read_csv(stcode+'.csv')
co = sd['close'].count()


for x in range(co-15,co):
	t = sd['date'][x]
	hp = sd['high'][x]
	lp = sd['low'][x]
	avp = (hp+lp)*0.5
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



'''
#for every price in s
bresults = []
for x in s:
	z = 0
	bb = {}	
	bb['price'] = x
	bb['bcount']=0
	bb['scount']=0
	for y in stock_data['price']:
		v = stock_data['volume'][z]
		tt = stock_data['type'][z]
		tt = tt.decode('utf-8')
		if (y==x) and (v>=100) and (tt==u"买盘"):			
			bb['bcount']+=v
		elif (y==x) and (v>=100) and (tt==u"卖盘"):			
			bb['scount']+=v
		else:
			z += 1
			continue
		z += 1
	bresults.append(bb)	

for x in bresults:
	#print x
	if (x['bcount']!=0) and (x['scount']!=0):
		print u"价格:",x['price'],u" 大买单总手:",x['bcount'],u" 大卖单总手:",x['scount']

'''