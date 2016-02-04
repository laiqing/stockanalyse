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

stlists = getnewstlist()
for x in stlists:
	wm = calcMacd(x['stcode'])
	wh = calcHighMacd(x['stcode'])
	kdj = calcKDJ(x['stcode'])
	if (wm>0) and (wh==1):
		print x['stcode'],x['stname']