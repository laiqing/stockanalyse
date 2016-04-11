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
import matplotlib.pyplot as plt  
import matplotlib.patches as patches


def getnewstlist():	
	f = codecs.open('allstdata3.json','r',encoding='utf-8')
	sss = json.loads(f.read())
	f.close()
	return sss

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
	#print "diff:",yesterdayk,k
	#print "dea",yesterdayd,d
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

def calcMACDback(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_weekewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_weekewma.csv')
	co = stock_data['close'].count()
	if co<=30:
		return 0
	l = range(1,co-1)
	l.reverse()
	if stock_data['DIFF'][co-1]>stock_data['DEA'][co-1]:
		jincha1 = co-1
		for x in l:
			if stock_data['DIFF'][x]<stock_data['DEA'][x]:
				#jincha dian
				jincha1 = x
				break
		sicha1 = jincha1-1
		l2 = range(1,jincha1)
		l2.reverse()
		for x in l2:
			if stock_data['DIFF'][x]>stock_data['DEA'][x]:
				#sicha1
				sicha1 = x
				break
		jincha2 = sicha1-1
		l3 = range(1,sicha1)
		l3.reverse()
		for x in l3:
			if stock_data['DIFF'][x]<stock_data['DEA'][x]:
				#jincha dian
				jincha2 = x
				break
		sicha2 = jincha2-1
		l4 = range(1,jincha2)
		l4.reverse()
		for x in l4:
			if stock_data['DIFF'][x]>stock_data['DEA'][x]:
				sicha2 = x
				break				
		#get 2 low point
		difflow1 = stock_data['DIFF'][sicha2]
		date1 = sicha2
		for x in range(sicha2,jincha2):
			if difflow1>stock_data['DIFF'][x]:
				difflow1 = stock_data['DIFF'][x]
				date1 = x
		difflow2 = stock_data['DIFF'][sicha1]
		date2 = sicha1
		for x in range(sicha1,jincha1):
			if difflow2>stock_data['DIFF'][x]:
				difflow2=stock_data['DIFF'][x]
				date2 = x
		close1 = stock_data['low'][date1]
		close2 = stock_data['low'][date2]
		if (close1 <= close2) and (difflow1>difflow2):
			return 1
	
	return 0


def calcKDJback(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_weekewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_weekewma.csv')
	co = stock_data['close'].count()
	if co<=30:
		return 0
	l = range(1,co-1)
	l.reverse()
	if stock_data['quick_d'][co-1]>stock_data['slow_d'][co-1]:
		jincha1 = co-1
		for x in l:
			if stock_data['quick_d'][x]<stock_data['slow_d'][x]:
				#jincha dian
				jincha1 = x
				break
		sicha1 = jincha1-1
		l2 = range(1,jincha1)
		l2.reverse()
		for x in l2:
			if stock_data['quick_d'][x]>stock_data['slow_d'][x]:
				#sicha1
				sicha1 = x
				break
		jincha2 = sicha1-1
		l3 = range(1,sicha1)
		l3.reverse()
		for x in l3:
			if stock_data['quick_d'][x]<stock_data['slow_d'][x]:
				#jincha dian
				jincha2 = x
				break
		sicha2 = jincha2-1
		l4 = range(1,jincha2)
		l4.reverse()
		for x in l4:
			if stock_data['quick_d'][x]>stock_data['slow_d'][x]:
				sicha2 = x
				break				
		#get 2 low point
		difflow1 = stock_data['quick_d'][sicha2]
		date1 = sicha2
		for x in range(sicha2,jincha2):
			if difflow1>stock_data['quick_d'][x]:
				difflow1 = stock_data['quick_d'][x]
				date1 = x
		difflow2 = stock_data['quick_d'][sicha1]
		date2 = sicha1
		for x in range(sicha1,jincha1):
			if difflow2>stock_data['quick_d'][x]:
				difflow2=stock_data['quick_d'][x]
				date2 = x
		close1 = stock_data['low'][date1]
		close2 = stock_data['low'][date2]
		if (close1 <= close2) and (difflow1>difflow2):
			return 1
	
	return 0


def calcKDJ(stockCode):
	#KDJ params is 9 , 3
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_ewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_ewma.csv')
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

def addChaYi(stockCode):
	#KDJ params is 9 , 3
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_ewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_ewma.csv')
	stock_data['diverse10']=numpy.round(map(lambda x,y:x/y-1,stock_data['close'],stock_data['EMA10']),4)
	co = stock_data['close'].count()
	lz = range(1,co)
	fir = stock_data['diverse10'][co-1]
	for x in lz:
		if :
			pass

	stock_data.to_csv(stockCode+'_d10.csv')
	

def emacross(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_ewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_ewma.csv')
	co = stock_data['close'].count()
	if co<=30:
		return 0
	e51 = stock_data['EMA5'][co-1]
	e52 = stock_data['EMA5'][co-2]
	e101 = stock_data['EMA10'][co-1]
	e102 = stock_data['EMA10'][co-2]
	if (e52>e51) and (e101>e102) and (e52<e102) and (e51>e101):
		return 1
	else:
		return 0

def getzhenfu(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_ewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_ewma.csv')
	co = stock_data['close'].count()
	lo = stock_data['low'][co-1]
	hi = stock_data['high'][co-1]
	res = numpy.round((hi-lo)/lo*100,2)
	return res

def getdiffyu(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_weekewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_weekewma.csv')
	co = stock_data['close'].count()
	d1 = stock_data['DIFF'][co-2]
	de1 = stock_data['DEA'][co-2]
	d2 = stock_data['DIFF'][co-1]
	de2 = stock_data['DEA'][co-1]
	y1 = d1 - de1
	y2 = d2 - de2
	if (y1/y2)>=3:
		return 1
	else:
		return 0

def get1231val(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_weekewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_weekewma.csv')
	al = stock_data['close'].count()
	if al<30:
		return 0
	#14,21,28
	co = 0
	i = 0
	for x in stock_data['date']:
		if x=='2015-12-14':
			co = i
			break
		i += 1
	if (co==0) or (co>(al-3)):
		return 0
	d1 = stock_data['DIFF'][co]
	d2 = stock_data['DIFF'][co+1]
	d3 = stock_data['DIFF'][co+2]
	de1 = stock_data['DEA'][co]
	de2 = stock_data['DEA'][co+1]
	de3 = stock_data['DEA'][co+2]
	v1 = d1 - de1
	v2 = d2 - de2
	v3 = d3 - de3
	if (v1<0) and (v1<v2) and (v2<v3) and (v3>0.5):
		return 1
	else:
		return 0


def chaoDi(stockCode):
	#chao di
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_ewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_ewma.csv')
	co = stock_data['close'].count()	
	if co<=30:
		return 0
	#per = stock_data['percent'][co-1]
	#print "percent:",per
	mco = stock_data['MA3'].count()
	eco = stock_data['EMA5'].count()
	todayclose = stock_data['close'][co-1]
	ma3 = stock_data['MA3'][co-1]
	#todayclose > 1.055*ma3 , low > ref(high,1) , v > ref(v,1)*1.2 , c > ma(c,5)
	ema5 = stock_data['EMA5'][co-1]
	todayv = stock_data['volume'][co-1]
	yesterdayv = stock_data['volume'][co-2]
	threedayv = stock_data['volume'][co-3]
	fourdayv = stock_data['volume'][co-4]
	#todaylow = stock_data['low'][co-1]
	#yesterdayhigh = stock_data['high'][co-2]
	#remove the todaylow > yesterdayhigh , it means tiaokong
	#if (todayclose > ma3*1.055) and (todayclose > ema5) and  (todayv > yesterdayv*1.2) and (yesterdayv>threedayv*1.2):
	if (todayclose > ema5) and  (todayv > yesterdayv*1.2) and (yesterdayv>threedayv*1.2) and (threedayv>fourdayv*3):
		return 1
	else:
		return 0

def calcWeekMacdDiff(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_weekewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_weekewma.csv')
	co = stock_data['close'].count()
	if co<=30:
		return 0

	#check if macd preview is si cha
	l = range(1,co-1)
	l.reverse()
	if stock_data['DIFF'][co-1]>stock_data['DEA'][co-1]:
		#jin cha
		return 0
	else:
		#pre is si cha
		diff0 = stock_data['DIFF'][co-1] - stock_data['DEA'][co-1]
		diff1 = stock_data['DIFF'][co-2] - stock_data['DEA'][co-2]
		diff2 = stock_data['DIFF'][co-3] - stock_data['DEA'][co-3]
		perd = diff0/stock_data['DEA'][co-1]
		#diff3 = stock_data['DIFF'][co-4] - stock_data['DEA'][co-4]	
		if (diff0>diff1) and (diff1>diff2) and (diff0>=-0.3):
			return 1
		else:
			return 0



def getfourbigsanwu(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_ewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_ewma.csv')
	co = stock_data['close'].count()	
	if co<=30:
		return 0
	low4 = stock_data['low'][co-4]
	h1 = stock_data['high'][co-1]
	per = (h1-low4)/low4
	return per
	
def drawMACD(stockCode):
	fig1 = plt.figure()
	ax1 = fig1.add_subplot(111, aspect='equal')
	ax1.set_xlim([0,400])
	ax1.set_ylim([-10,10])
	stock_data = pandas.read_csv(stockCode+'_weekewma.csv')
	co = stock_data['close'].count()
	xr = range(1,co)
	diffr = []
	dear = []
	for x in xr:
		diffr.append(stock_data['DIFF'][x])
		dear.append(stock_data['DEA'][x])
	plt.plot(xr,diffr,'y')
	plt.plot(xr,dear,'b')
	plt.legend()
	plt.show()



#drawMACD('sz300187')

addChaYi('sz300187')

'''

stlists = getnewstlist()
for x in stlists:
	#print "proc:",x['stcode']
	wm = calcMacd(x['stcode'])
	wh = calcHighMacd(x['stcode'])
	wmb = calcMACDback(x['stcode'])
	rc = getzhenfu(x['stcode'])
	yu = getdiffyu(x['stcode'])

	#if yu==1:
	#	print x['stcode'],wm,wh,wmb

	#if (wm>=25) and (wh==1):
	#	print x['stcode'],wm," high value: ",wh," macd back: ",wmb, " ri zhen fu: ",rc

	#pe = getfourbigsanwu(x['stcode'])
	#if (pe>=0.32):
	#	print "pe>0.32:",x['stcode']," pe: ", pe, " ri zhen fu: ",rc

	p = get1231val(x['stcode'])
	if p==1:
		print x['stcode']


	#yy = emacross(x['stcode'])
	#if yy==1:
	#	print x['stcode']






	#if (x['stcode']=='SH600113'):
	#	print x['stcode'],wm," high value: ",wh," back :",wmb
	#	break


	#kdj = calcKDJ(x['stcode'])
	#cd = chaoDi(x['stcode'])
	#cw = calcWeekMacdDiff(x['stcode'])
	#if (cw==1) and (wh>0):
	#	print x['stcode'],wh," volume: ",cd
	#pe = getfourbigsanwu(x['stcode'])
	#if (cd==1):
	#	print x['stcode'],x['stname'],"macd:",wm," macd high:",wh, " kdj:",kdj
	#if pe>=0.35:
	#	print x['stcode'],x['stname']
	#if x['stcode']=="SZ002466":
	#	print x['stcode'],x['stname'],pe
	#if (pe>=0.35):
	#	print x['stcode'],x['stname']

'''