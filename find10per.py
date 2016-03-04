# coding = utf-8 

import urllib,urllib2
import httplib
import shutil
import os
import sys
import linecache
import codecs
import cookielib
from HTMLParser import HTMLParser
import numpy
import pandas
import time
from multiprocessing.dummy import Pool as ThreadPool
import socket
import json
socket.setdefaulttimeout(10.0) 

def getnewstlist():
	stslists = []
	f = codecs.open('allstdata3.json','r',encoding='utf-8')
	sss = json.loads(f.read())
	for x in sss:
		stslists.append(x['stcode'])
	return stslists

	
	

def getlist():
	#down csv from xueqiu
	#newlists = getnewstlist()
	f = codecs.open('allstdata3.json','r',encoding='utf-8')
	sss = json.loads(f.read(),encoding='utf-8')
	f.close()
	su = 0
	count = 0
	pmin = 0
	pmax = 0
	xmin = []
	for x in sss:
		
		if os.path.exists(x['stcode']+'_ewma.csv')==False:
			continue
		#print "process:",x
		stock_data = pandas.read_csv(x['stcode']+'_ewma.csv')		
		co = stock_data['close'].count()
		if co<=30:
			continue
		if str(stock_data['date'][co-1])!="2016-01-28":
			continue
		#find today
		count += 1
		d = stock_data['EMA10'][co-1]
		vv = stock_data['close'][co-1]
		pp = float(d)/float(vv)
		su += pp
		if pp>pmax:
			pmax = pp
		if pmin==0:
			pmin = pp
		elif pp<pmin:
			pmin = pp
		if pp<1:
			xmin.append(x['stcode'])
		
		'''	
		day = time.strftime('%d',time.localtime())	
		mo = time.strftime('%m',time.localtime())
		too = time.strftime('%Y',time.localtime())
		today = too+"-"+mo+"-"+day
		if len(sys.argv)>1:
			today = sys.argv[1]
		
		d = stock_data['EMA10'][co-1]
		vv = stock_data['close'][co-1]
		pp = float(d)/float(vv)
		if pp>=1.15:
			print "find: ",x['stcode'],"-- diverse: ",pp

		
		d2 = stock_data['EMA250'][co-1]
		pp2 = float(vv)-float(d2)
		if (pp2<=1) and (pp2>0):
			print "year line:",x['stcode'],"--",pp2
		'''
	av = su/count
	print av
	print pmin
	print pmax
	print xmin

getlist()
	
