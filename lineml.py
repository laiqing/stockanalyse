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

from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import svm
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeRegressor  
from sklearn.ensemble import RandomForestRegressor  
from sklearn.neighbors import KNeighborsRegressor



def readBigDeal(stock_data,lastclose,totalshare):
	prebuyprice = 0
	presellprice = 0
	lstime = 0
	pstime = 0
	co = stock_data['volume'].count()
	lz = range(1,co-1)
	lz.reverse()
	tmp = []
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
					#add to data
					npercent = p/lastclose-1
					nvolume = vo/totalshare
					tmp.append([npercent,nvolume,1])					
					#ndata = tmp					
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
					npercent = p/lastclose-1
					nvolume = vo/totalshare
					tmp.append([npercent,nvolume,-1])					
					#ndata = tmp
					print "down ",stock_data['time'][x]," price: ",stock_data['price'][x]," count: ",vo
					pstime += 1
				presellprice = p
			else:
				presellprice = stock_data['price'][x]
	print "up time:",lstime
	print "down time:",pstime
	df = pandas.DataFrame(tmp,columns=['percent','volume','direction'])
	return df


def readStockInfoToX(stcode):
	data2 = pandas.read_csv(stcode+'.csv')
	co = data2['close'].count()
	tmp = []
	for x in range(0,co-11):		
		tmp.append([data2['open'][x],data2['close'][x],data2['high'][x],data2['low'][x],data2['open'][x+1],data2['close'][x+1],data2['high'][x+1],data2['low'][x+1],data2['open'][x+2],data2['close'][x+2],data2['high'][x+2],data2['low'][x+2],data2['open'][x+3],data2['close'][x+3],data2['high'][x+3],data2['low'][x+3],data2['open'][x+4],data2['close'][x+4],data2['high'][x+4],data2['low'][x+4],data2['open'][x+5],data2['close'][x+5],data2['high'][x+5],data2['low'][x+5],data2['open'][x+6],data2['close'][x+6],data2['high'][x+6],data2['low'][x+6],data2['open'][x+7],data2['close'][x+7],data2['high'][x+7],data2['low'][x+7],data2['open'][x+8],data2['close'][x+8],data2['high'][x+8],data2['low'][x+8],data2['open'][x+9],data2['close'][x+9],data2['high'][x+9],data2['low'][x+9]])		
	return tmp

def readStockInfoToY(stcode):
	data2 = pandas.read_csv(stcode+'.csv')
	co = data2['close'].count()
	tmp = []
	for x in range(10,co-1):		
		tmp.append(data2['high'][x])
	return tmp

def readStockInfoOpenToY(stcode):
	data2 = pandas.read_csv(stcode+'.csv')
	co = data2['close'].count()
	tmp = []
	for x in range(10,co-1):		
		tmp.append(data2['open'][x])
	return tmp

def readStockInfoCloseToY(stcode):
	data2 = pandas.read_csv(stcode+'.csv')
	co = data2['close'].count()
	tmp = []
	for x in range(10,co-1):		
		tmp.append(data2['close'][x])
	return tmp

def readStockInfoLowToY(stcode):
	data2 = pandas.read_csv(stcode+'.csv')
	co = data2['close'].count()
	tmp = []
	for x in range(10,co-1):		
		tmp.append(data2['low'][x])
	return tmp


def readStockLastInfoToX(stcode):
	data2 = pandas.read_csv(stcode+'.csv')
	co = data2['close'].count()
	tmp = []
	x = co-10
	tmp.append([data2['open'][x],data2['close'][x],data2['high'][x],data2['low'][x],data2['open'][x+1],data2['close'][x+1],data2['high'][x+1],data2['low'][x+1],data2['open'][x+2],data2['close'][x+2],data2['high'][x+2],data2['low'][x+2],data2['open'][x+3],data2['close'][x+3],data2['high'][x+3],data2['low'][x+3],data2['open'][x+4],data2['close'][x+4],data2['high'][x+4],data2['low'][x+4],data2['open'][x+5],data2['close'][x+5],data2['high'][x+5],data2['low'][x+5],data2['open'][x+6],data2['close'][x+6],data2['high'][x+6],data2['low'][x+6],data2['open'][x+7],data2['close'][x+7],data2['high'][x+7],data2['low'][x+7],data2['open'][x+8],data2['close'][x+8],data2['high'][x+8],data2['low'][x+8],data2['open'][x+9],data2['close'][x+9],data2['high'][x+9],data2['low'][x+9]])		
	return tmp


def readStockInfoToX2(stcode):
	data2 = pandas.read_csv(stcode+'.csv')
	co = data2['close'].count()
	tmp = []
	for x in range(0,co-11):		
		tmp.append([data2['open'][x],data2['close'][x],data2['high'][x],data2['low'][x],data2['open'][x+1],data2['close'][x+1],data2['high'][x+1],data2['low'][x+1],data2['open'][x+2],data2['close'][x+2],data2['high'][x+2],data2['low'][x+2],data2['open'][x+3],data2['close'][x+3],data2['high'][x+3],data2['low'][x+3],data2['open'][x+4],data2['close'][x+4],data2['high'][x+4],data2['low'][x+4],data2['open'][x+5],data2['close'][x+5],data2['high'][x+5],data2['low'][x+5],data2['open'][x+6],data2['close'][x+6],data2['high'][x+6],data2['low'][x+6],data2['open'][x+7],data2['close'][x+7],data2['high'][x+7],data2['low'][x+7],data2['open'][x+8],data2['close'][x+8],data2['high'][x+8],data2['low'][x+8],data2['open'][x+9],data2['close'][x+9],data2['high'][x+9],data2['low'][x+9]])		
	df = pandas.DataFrame(tmp,columns=['open1','close1','high1','low1','open2','close2','high2','low2','open3','close3','high3','low3','open4','close4','high4','low4','open5','close5','high5','low5','open6','close6','high6','low6','open7','close7','high7','low7','open8','close8','high8','low8','open9','close9','high9','low9','open10','close10','high10','low10'])
	return df


def readStockLastInfoToX2(stcode):
	data2 = pandas.read_csv(stcode+'.csv')
	co = data2['close'].count()
	tmp = []
	x = co-10
	tmp.append([data2['open'][x],data2['close'][x],data2['high'][x],data2['low'][x],data2['open'][x+1],data2['close'][x+1],data2['high'][x+1],data2['low'][x+1],data2['open'][x+2],data2['close'][x+2],data2['high'][x+2],data2['low'][x+2],data2['open'][x+3],data2['close'][x+3],data2['high'][x+3],data2['low'][x+3],data2['open'][x+4],data2['close'][x+4],data2['high'][x+4],data2['low'][x+4],data2['open'][x+5],data2['close'][x+5],data2['high'][x+5],data2['low'][x+5],data2['open'][x+6],data2['close'][x+6],data2['high'][x+6],data2['low'][x+6],data2['open'][x+7],data2['close'][x+7],data2['high'][x+7],data2['low'][x+7],data2['open'][x+8],data2['close'][x+8],data2['high'][x+8],data2['low'][x+8],data2['open'][x+9],data2['close'][x+9],data2['high'][x+9],data2['low'][x+9]])		
	df = pandas.DataFrame(tmp,columns=['open1','close1','high1','low1','open2','close2','high2','low2','open3','close3','high3','low3','open4','close4','high4','low4','open5','close5','high5','low5','open6','close6','high6','low6','open7','close7','high7','low7','open8','close8','high8','low8','open9','close9','high9','low9','open10','close10','high10','low10'])
	return df


def getLastClose(stcode):
	data2 = pandas.read_csv(stcode+'.csv')
	co = data2['close'].count()
	return data2['close'][co-1]
		

#st='sz300264'
t = time.strftime('%Y-%m-%d',time.localtime())
st = sys.argv[1]
print st," ",t,u" 股价预测:"

z = getLastClose(st)

xdata = readStockInfoToX(st)
ydata = readStockInfoToY(st)
ydata2 = readStockInfoOpenToY(st)
ydata3 = readStockInfoCloseToY(st)
ydata4 = readStockInfoLowToY(st)

xx = readStockLastInfoToX(st)

linreg = LinearRegression()
linreg.fit(xdata, ydata)
linreg2 = LinearRegression()
linreg2.fit(xdata, ydata2)
linreg3 = LinearRegression()
linreg3.fit(xdata, ydata3)
linreg4 = LinearRegression()
linreg4.fit(xdata, ydata4)


th = linreg.predict(xx)
to = linreg2.predict(xx)
tc = linreg3.predict(xx)
tl = linreg4.predict(xx)


todayopen = numpy.round(to[0],2)
todayclose = numpy.round(tc[0],2)
todayhigh = numpy.round(th[0],2)
todaylow = numpy.round(tl[0],2)

print u"线性回归预测:"
print u"开盘价:", todayopen
print u"收盘价:",todayclose
print u"最高价:" ,todayhigh
print u"最低价", todaylow
#print per2,per3,per,per4


'''
rf = RandomForestRegressor()  
rf.fit(xdata,ydata)
rf2 = RandomForestRegressor()  
rf2.fit(xdata,ydata2)
rf3 = RandomForestRegressor()  
rf3.fit(xdata,ydata3)
rf4 = RandomForestRegressor()  
rf4.fit(xdata,ydata4)


todayhigh = rf.predict(xx)
todayopen = rf2.predict(xx)
todayclose = rf3.predict(xx)
todaylow = rf4.predict(xx)
per = numpy.round(todayhigh/z,4)-1
per2 = numpy.round(todayopen/z,4)-1
per3 = numpy.round(todayclose/z,4)-1
per4 = numpy.round(todaylow/z,4)-1

print "Random Forest Regressor:",todayopen, todayclose, todayhigh, todaylow
print per2,per3,per,per4
'''
'''
model = KNeighborsRegressor()
model.fit(xdata,ydata)
model2 = KNeighborsRegressor()
model2.fit(xdata,ydata2)
model3 = KNeighborsRegressor()
model3.fit(xdata,ydata3)
model4 = KNeighborsRegressor()
model4.fit(xdata,ydata4)


todayhigh = model.predict(xx)
todayopen = model2.predict(xx)
todayclose = model3.predict(xx)
todaylow = model4.predict(xx)
per = numpy.round(todayhigh/z,4)-1
per2 = numpy.round(todayopen/z,4)-1
per3 = numpy.round(todayclose/z,4)-1
per4 = numpy.round(todaylow/z,4)-1

print "KNN:",todayopen, todayclose, todayhigh, todaylow
print per2,per3,per,per4
'''

'''
xdata2 = readStockInfoToX2(st)
xx2 = readStockLastInfoToX2(st)
clf = LinearSVC()

ydata2 = map(lambda x:x*100,ydata)
ydata3 = numpy.array(ydata2).astype(int)

clf.fit(xdata2,ydata3)
th2 = clf.predict(xx2)
print st," -- SVM today high:",th2
'''


'''
preclose = 26.01
totalr = 2610000.0
todayclose = 26.2/preclose - 1

#read the pandas
data = pandas.read_csv('sz300052_2016-03-25_trade.csv')

traindata = []

#ndata = pandas.DataFrame(columns=['percent','volume','direction'])

ndata = readBigDeal(data,preclose,totalr)

ys = []
for x in ndata['percent']:
	ys.append(x)
ys.append(todayclose)

del ys[0]


preclose = 26.31
todayclose = 25.13/preclose - 1

data2 = pandas.read_csv('sz300052_2016-03-29_trade.csv')
ndata2 = readBigDeal(data2,preclose,totalr)


ys2 = []
for x in ndata2['percent']:
	ys2.append(x)
ys2.append(todayclose)

del ys2[0]


linreg = LinearRegression()
linreg.fit(ndata, ys)

print linreg.intercept_
print linreg.coef_

clf = LinearSVC()
clf.fit(ndata,ys)

t = clf.predict(ndata2[0])
print t

#y_pred = linreg.predict(ndata2)

#print ys2
#print y_pred
'''
print "finish!"

