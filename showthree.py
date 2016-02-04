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
socket.setdefaulttimeout(10.0) 
import matplotlib.pyplot as plt  
import matplotlib.patches as patches


fig1 = plt.figure()
ax1 = fig1.add_subplot(111, aspect='equal')
ax1.set_xlim([0,100])
ax1.set_ylim([0,60])


stockCode = sys.argv[1]
#dt = sys.argv[2]
stock_data = pandas.read_csv(stockCode+'.csv')
co = stock_data['close'].count()

r = range(co-99,co)

first = stock_data['close'][co-100]
prehigh = first
prelow = first
premiddle = first

st = 0
set2 = 0
prerise = 0
for x in r:
	if st==0:
		#first point
		curr = stock_data['close'][x]
		if first<curr:
			#raise
			rect = patches.Rectangle(xy=(st,first),width=1,height=curr-first,facecolor="red")
			ax1.add_patch(rect)
			prelow = first
			prehigh = curr
			prerise = 1

		else:
			#down
			rect = patches.Rectangle(xy=(st,curr),width=1,height=first-curr,facecolor="green")
			ax1.add_patch(rect)
			prelow = curr
			prehigh = first
			prerise = 0
		st += 1

	elif set2==0:
		#second point
		curr = stock_data['close'][x]
		if curr>prehigh:
			#raise
			rect = patches.Rectangle(xy=(st,prehigh),width=1,height=curr-prehigh,facecolor="red")
			ax1.add_patch(rect)
			premiddle = prehigh
			prehigh = curr			
			set2 = 1
			st +=1
			prerise = 1

		elif (curr<prehigh) and (curr>prelow):
			#down but not low than prelow do nothing
			pass
		else:
			rect = patches.Rectangle(xy=(st,curr),width=1,height=prelow-curr,facecolor="green")
			ax1.add_patch(rect)
			set2 = 1
			premiddle = prelow
			prelow = curr
			st += 1
			prerise = 0

	else:
		#other points
		curr = stock_data['close'][x]
		if curr>prehigh:
			if prerise==1:				
				rect = patches.Rectangle(xy=(st,prehigh),width=1,height=curr-prehigh,facecolor="red")
				prelow = premiddle
				premiddle = prehigh
				prehigh = curr
			else:
				rect = patches.Rectangle(xy=(st,prehigh),width=1,height=curr-premiddle,facecolor="red")				
				prehigh = curr
			ax1.add_patch(rect)			
			st += 1
			prerise = 1
		elif (curr<prehigh) and (curr>prelow):
			pass
		else:
			if prerise==1:
				rect = patches.Rectangle(xy=(st,curr),width=1,height=premiddle-curr,facecolor="green")
				prelow = curr				
			else:
				rect = patches.Rectangle(xy=(st,curr),width=1,height=prelow-curr,facecolor="green")				
				premiddle = prelow
				prehigh = premiddle
				prelow = curr
			ax1.add_patch(rect)
			
			st += 1
			prerise = 0

	



#rect = patches.Rectangle(xy=(0,1),width=1,height=5,facecolor="red")
#ax1.add_patch(rect)
plt.show()

'''
xr = xrange(0,60)
idx = stock_data['lowdiffmacd'].count()-60
yr = stock_data['lowdiffmacd'][idx:]
plt.plot(xr,yr,'r')
plt.legend()
plt.show()
'''

'''
s = ""
for x in xrange(2588,2787):
	s += "'sz00"+str(x)+"',"
print s
'''
