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

print "usage: verifydate.py 2015-12-11"
verifyday = sys.argv[1]
client = pymongo.MongoClient('mongodb://jiucaidiowner:jiucaidi1976@ds059644.mongolab.com:59644/jiucaidi?authMechanism=SCRAM-SHA-1')
tablename = verifyday.replace('-','')
datas = client.jiucaidi[tablename]
items = datas.find()

f = open('verify'+tablename+'.csv','w')


for x in items:	
	#now read the csv file and get the last 2 days percent
	tcode = x['stcode']
	if len(tcode)==6:
		if tcode[0]=='0':
			tcode = 'sz'+tcode
		elif tcode[0]=='3':
			tcode = 'sz'+tcode
		else:
			tcode = 'sh'+tcode
	print tcode

	
	pa = os.getcwd()
	if os.path.exists(pa+'/'+tcode+'_ewma.csv')==False:
		print tcode,"no history data for this stock"
		continue
	stock_data = pandas.read_csv(tcode+'_ewma.csv')
	co = stock_data['close'].count()
	if co<30:
		print tcode,"new stock, no need for analyse"
		continue
	xr = range(1,co)
	found = co-1
	for i in xr:
		d = stock_data['date'][co-i]
		if d==verifyday:
			found = co-i
			break
	xr = range(found+1,co)
	arr = ""
	total = 1
	tstr = str(tcode)
	for i in xr:
		arr += "\t"+str(stock_data['percent'][i]*100)
		total = total*(1+stock_data['percent'][i])
		tstr += ","+str(stock_data['percent'][i]*100)
	tstr = tstr + "," + str((total-1)*100) + "\n"
	total = numpy.round((total-1)*100,2)
	print tcode,arr,"\t",total
	f.write(tstr)


f.close()

print "finish"


		
