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

#reload(sys)
#sys.setdefaultencoding('utf-8')
#predicts=['300156','300098','300187','300120','300055','300202','300175','600873','600362','600498','600159','600497','601113','600697','600010','600655','601600','600728','601808','600449','600298','601158','002034','002436','000488','000540','002156','002081','002632','002281','000089','002671','002051','002383','000758','000509','000680','002686','002089','000960','002393','002185','002414','000517','000987','002338','000063','002692','000166','000823','000581','002465','002736']

client = pymongo.MongoClient('mongodb://jiucaidiowner:jiucaidi1976@ds059644.mongolab.com:59644/jiucaidi?authMechanism=SCRAM-SHA-1')

upinfo = time.strftime('%Y%m%d',time.localtime())
datas = client.jiucaidi[upinfo]
datas.remove()

datas2 = client.jiucaidi['everydaycy']
items = datas2.find()
items.sort('kdj',pymongo.DESCENDING)
res=[]
for x in items:
	if (x['kdj']>0) and (x['kdjback']==1):
		res.append(x)


datas2 = client.jiucaidi['everydaysh']
items = datas2.find()
items.sort('kdj',pymongo.DESCENDING)
for x in items:
	if (x['kdj']>0) and (x['kdjback']==1):
		res.append(x)

datas2 = client.jiucaidi['everydaysz']
items = datas2.find()
items.sort('kdj',pymongo.DESCENDING)
for x in items:
	if (x['kdj']>0) and (x['kdjback']==1):
		res.append(x)


gn = []
for x in res:
	aa = {}
	aa['stcode']=x['stcode']
	gn.append(aa)

if len(res)>0:
	print "now insert results...",len(res)
	datas.insert(res)




