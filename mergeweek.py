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
import re
socket.setdefaulttimeout(10.0) 
from bson import BSON
from bson import json_util
from datetime import datetime, timedelta


def getnewstlist():	
	f = codecs.open('allstdata3.json','r',encoding='utf-8')
	sss = json.loads(f.read())
	f.close()
	return sss

#now merge
def genweek(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'.csv')==False:
		return
	stock_data = pandas.read_csv(stockCode+'.csv')
	if stock_data['close'].count()==0:
		print stockCode," data empty, maybe exist stock market"
		return

	weekhigh = stock_data['high'][0]
	weeklow = stock_data['low'][0]
	weekopen = stock_data['open'][0]
	weekclose = stock_data['close'][0]
	weekvolume = 0
	weekmonday = stock_data['date'][0]
	weeks = []
	weekhighs = []
	weeklows = []
	weekopens = []
	weekcloses = []
	weekvols = []
	co = 0
	fir = stock_data['date'][0]		
	for x in stock_data['date']:
		#check the continue's date , if not continue, then check if in the same week, else new week, if continue then in the same week		
		ystr = int(fir[:4])
		mstr = int(fir[5:][:2])
		dstr = int(fir[8:][:2])
		fd = datetime(ystr,mstr,dstr)
		tystr = int(x[:4])
		tmstr = int(x[5:][:2])
		tdstr = int(x[8:][:2])
		td = datetime(tystr,tmstr,tdstr)
		stmonday1 =  (fd - timedelta(days=fd.weekday()))
		stmonday2 =  (td - timedelta(days=td.weekday()))
		yushu = (stmonday2-stmonday1).days/7
		if yushu==0:
			#same week
			weekclose = stock_data['close'][co]
			if weekhigh < stock_data['high'][co]:
				weekhigh = stock_data['high'][co]
			if weeklow > stock_data['low'][co]:
				weeklow = stock_data['low'][co]
			weekvolume += stock_data['volume'][co]
		else:
			#new week
			weeks.append(fir)
			weekhighs.append(weekhigh)
			weeklows.append(weeklow)
			weekopens.append(weekopen)
			weekcloses.append(weekclose)
			weekvols.append(weekvolume)
			weekhigh = stock_data['high'][co]
			weeklow = stock_data['low'][co]
			weekopen = stock_data['open'][co]
			weekclose = stock_data['close'][co]
			weekvolume = stock_data['volume'][co]
			fir = stock_data['date'][co]
		co += 1
	#add the final weekday
	cu = len(weekopens)
	if weekopen != weekopens[cu-1]:
		weeks.append(fir)
		weekhighs.append(weekhigh)
		weeklows.append(weeklow)
		weekopens.append(weekopen)
		weekcloses.append(weekclose)
		weekvols.append(weekvolume)
			
	datas = list(zip(weeks,weekopens,weekhighs,weeklows,weekcloses,weekvols))
	df = pandas.DataFrame(data=datas,columns=['date','open','high','low','close','volume'])
	df.to_csv(stockCode+'_week.csv')


def calcAllInstructor(stockCode):
	#MACD params is 5,10,7	
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_week.csv')==False:
		print stockCode," week data not exists"
		return
	stock_data = pandas.read_csv(stockCode+'_week.csv')
	if stock_data['close'].count()==0:
		print stockCode," data empty, maybe exist stock market"
		return

	stock_data['amplitude'] = numpy.round(stock_data['close'].diff(),3)
	stock_data['percent'] = numpy.round(stock_data['close'].pct_change(),4)		
	stock_data['MA3'] = numpy.round(pandas.rolling_mean(stock_data['close'],3),3)
	stock_data['EMA5'] = numpy.round(pandas.ewma(stock_data['close'],span=5),3)
	stock_data['EMA10'] = numpy.round(pandas.ewma(stock_data['close'],span=10),3)	
	stock_data['EMA20'] = numpy.round(pandas.ewma(stock_data['close'],span=20),3)	
	stock_data['EMA22'] = numpy.round(pandas.ewma(stock_data['close'],span=22),3)	
	stock_data['DIFF'] = map(lambda x,y:x-y, stock_data['EMA10'],stock_data['EMA22'])
	stock_data['DEA'] = numpy.round(pandas.rolling_mean(stock_data['DIFF'],7),3)

	stock_data['abspercent'] = map(lambda x:x*100 ,stock_data['percent'])
	stock_data['EMA15PER'] = numpy.round(pandas.ewma(stock_data['abspercent'],span=15),3)

	#now KDJ params is 9,3,3
	stock_data['low9'] = pandas.rolling_min(stock_data['close'],9)
	stock_data['high9'] = pandas.rolling_max(stock_data['close'],9)
	stock_data['quick_k'] = map(lambda x,y,z:numpy.round((x-y)/(z-y)*100,2) if z>y else 0, stock_data['close'],stock_data['low9'],stock_data['high9'])
	stock_data['quick_d'] = numpy.round(pandas.rolling_mean(stock_data['quick_k'],3),2)
	stock_data['slow_d'] = numpy.round(pandas.rolling_mean(stock_data['quick_d'],3),2)

	#calc low open diff
	stock_data['maxclosediff'] = map(lambda x: x if x>0 else 0, stock_data['amplitude'])
	stock_data['absclosediff'] = map(lambda x: x if x>0 else -x, stock_data['amplitude'])
	stock_data['fmrsi'] = numpy.round(pandas.ewma(stock_data['maxclosediff'],span=5),3)
	stock_data['fzrsi'] = numpy.round(pandas.ewma(stock_data['absclosediff'],span=5),3)
	stock_data['rsi5'] = numpy.round(map(lambda x,y: x/y*100, stock_data['fmrsi'],stock_data['fzrsi']),2)


	stock_data['bollstd'] = numpy.round(pandas.rolling_std(stock_data['close'],20),3)

	stock_data['jd'] = map(lambda x,y:x*y, stock_data['amplitude'],stock_data['volume'])
	stock_data['ejd'] = pandas.ewma(stock_data['jd'],span=3)	

	stock_data.to_csv(stockCode+'_weekewma.csv')


	
def calcMacd(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_weekewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_weekewma.csv')
	co = stock_data['close'].count()
	if co<=30:
		return 0
	sco = stock_data['DEA'].count()
	yesterdayk = stock_data['DIFF'][co-2]
	k = stock_data['DIFF'][co-1]
	yesterdayd = stock_data['DEA'][co-2]
	d = stock_data['DEA'][co-1]
	if (yesterdayk < yesterdayd) and (k>=d):
		#get the angle
		k1 = math.atan(d-yesterdayd)
		k2 = math.atan(k-yesterdayk)
		d1 = math.degrees(k1)
		d2 = math.degrees(k2)
		if d1<0:
			d1 = -d1	
		d = d1+d2
		if d>90:
			d = d-90		
		return numpy.round(d)
	else:
		return 0

def calcHighMacd(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_weekewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_weekewma.csv')
	co = stock_data['close'].count()
	if co<=30:
		return 0	
	k = stock_data['DIFF'][co-1]	
	d = stock_data['DEA'][co-1]
	if (k>0) and (d>0):
		return 1
	else:
		return 0
	

def calcKDJ(stockCode):
	#KDJ params is 9 , 3
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_weekewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_weekewma.csv')
	co = stock_data['close'].count()
	if co<=30:
		return 0
	#co = stock_data['quick_d'].count()
	sco = stock_data['slow_d'].count()
	yesterdayk = stock_data['quick_d'][co-2]
	k = stock_data['quick_d'][co-1]
	yesterdayd = stock_data['slow_d'][co-2]
	d = stock_data['slow_d'][co-1]
	if (yesterdayk < yesterdayd) and (k>=d):
		k1 = math.atan(d-yesterdayd)
		k2 = math.atan(k-yesterdayk)
		d1 = math.degrees(k1)
		d2 = math.degrees(k2)
		if d1<0:
			d1 = -d1
		d = d1+d2
		if d>90:
			d = d-90
		return numpy.round(d)
	else:
		return 0


def calcLowKDJ(stockCode):
	#KDJ params is 9 , 3
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_weekewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_weekewma.csv')
	co = stock_data['close'].count()
	if co<=30:
		return 0
	#co = stock_data['quick_d'].count()
	sco = stock_data['slow_d'].count()	
	k = stock_data['quick_d'][co-1]	
	d = stock_data['slow_d'][co-1]
	if (k<=20) and (d<=20):
		return 1
	else:
		return 0



stlists = getnewstlist()


for x in stlists:
	print "generate week data:",x['stcode']
	genweek(x['stcode'])
	calcAllInstructor(x['stcode'])

print "generate finish"
'''

for x in stlists:
	macd = calcMacd(x['stcode'])
	hi = calcHighMacd(x['stcode'])
	#kdj = calcKDJ(x['stcode'])
	#lkdj = calcLowKDJ(x['stcode'])
	if (macd>0) and (hi==1):
		print x['stcode'],x['stname']
	#if (kdj>0) and (lkdj==1):
	#	print x['stcode'],"--low kdj:",kdj," -- ",lkdj
'''

#names = ['Bob','Jessica','Mary','John','Mel','aa']
#births = [968, 155, 77, 578, 973,33]
#ages = [1,2,3,4,5,6]
#BabyDataSet = list(zip(names,births,ages))
#df = pandas.DataFrame(data = BabyDataSet, columns=['Names', 'Births','ages'])
#print df