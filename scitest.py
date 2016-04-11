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
import matplotlib

#import tushare as ts
from pandas.compat import StringIO

import scipy as sp


#myfont = matplotlib.font_manager.FontProperties(fname='C:/Windows/Fonts/msyh.ttf')  
#matplotlib.rcParams['axes.unicode_minus'] = False  

def onPick(event):
	ind = event.ind
	print "on pick:",ind

stcode = "sz002431"

day = "2016-04-01"

sd = pandas.read_csv(stcode+'_'+day+'_trade.csv')

i=0
xx = []
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
co = len(yy)
xx = range(0,co)

#plt.scatter(xx,yy)
xbar = plt.bar(xx,yy,0.5,color='r',picker=True)

i = 0
for b in xbar:
	if bb[i].decode('utf-8')==u"买盘":
		xbar[i].set_color('r')
	elif bb[i].decode('utf-8')==u"卖盘":
		xbar[i].set_color('g')
	else:
		xbar[i].set_color('y')
	i += 1

plt.title(stcode+" "+day)
plt.xlabel("tick")
plt.ylabel("Volume")

i = 0
for x in zz:
	h = xbar[i].get_height() + 10
	x1 = xbar[i].get_x()
	plt.text(x1,h,str(zz[i]))
	plt.text(x1,h+80,str(dd[i]))
	i += 1


#plt.xticks([w*7*24 for w in range(10)],['week %i'%w for w in range(10)])
plt.autoscale(tight=True)
plt.grid()
plt.show()

