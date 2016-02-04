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
socket.setdefaulttimeout(10.0) 




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

def calcMACD(stockCode):	
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_ewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_ewma.csv')
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


def calcMACDback(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_ewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_ewma.csv')
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
	if os.path.exists(pa+'/'+stockCode+'_ewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_ewma.csv')
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
	todaylow = stock_data['low'][co-1]
	yesterdayhigh = stock_data['high'][co-2]
	if (todayclose > ma3*1.055) and (todayclose > ema5) and (todaylow > yesterdayhigh) and (todayv > yesterdayv*1.2):
		return 1
	else:
		return 0


def chaoBaoLuo(stockCode):
	#chao guo baoluo xian
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_ewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_ewma.csv')
	co = stock_data['close'].count()
	if co<=30:
		return 0
	eco = stock_data['EMA14'].count()
	ema14 = stock_data['EMA14'][co-1]
	todayhigh = stock_data['high'][co-1]
	# high> 1.04*ema14, 
	if (todayhigh > ema14*1.04):
		return 1
	else:
		return 0

def getlowdiff(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_ewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_ewma.csv')
	co = stock_data['close'].count()		
	if co<=30:
		return 0
	ema14 = stock_data['EMA14'][co-1]
	cp = ema14 - stock_data['EMA14'][co-2]	
	return cp

def realChaoBaoLuo(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_ewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_ewma.csv')
	co = stock_data['close'].count()
	if co<=30:
		return 0
	eco = stock_data['EMA14'].count()
	mco = stock_data['MA3'].count()
	ema14 = stock_data['EMA14'][co-1]
	ma3 = stock_data['MA3'][co-1]
	lo = stock_data['low'][co-1]
	cp = ema14 - stock_data['EMA14'][co-2]
	lo2 = lo + cp	
	# high> 1.04*ema14, 
	if (ma3 > ema14*1.04):
		return 1
	else:
		return 0


def getRsi(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_ewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_ewma.csv')
	co = stock_data['close'].count()
	if co<=30:
		return 0
	rsi5 = stock_data['rsi5'][co-1]
	return rsi5


def getAmpli(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_ewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_ewma.csv')
	co = stock_data['close'].count()
	if co<=30:
		return 0
	#avp = stock_data['avgpriceema5'][co-1]
	avgdiff = stock_data['highlowdiffema5'][co-1]
	return avgdiff

def get30daysup(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_ewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_ewma.csv')
	co = stock_data['close'].count()
	if co<=30:
		return 0
	it = 0
	xt = co-30	
	if xt<0:
		return 0
	for x in range(xt,co):
		if stock_data['percent'][x]*100>5:
			it +=1
	return it

def getboll(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_ewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_ewma.csv')
	co = stock_data['close'].count()
	if co<=30:
		return 0
	ema14 = stock_data['EMA14'][co-1]
	bollstd = stock_data['bollstd'][co-1]
	hi = stock_data['high'][co-1]
	lo = stock_data['low'][co-1]
	if (hi>=(ema14+2*bollstd)):
		return 1
	elif (lo<=(ema14-2*bollstd)):
		return -1
	else:
		return 0

def getbollsign(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_ewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_ewma.csv')
	co = stock_data['close'].count()
	if co<=30:
		return 0
	bollstd0 = stock_data['bollstd'][co-2] 
	bollstd = stock_data['bollstd'][co-1]
	if bollstd>bollstd0:
		return 1
	else:
		return 0

def getpressandsupport(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_ewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_ewma.csv')
	co = stock_data['close'].count()
	if co<=30:
		return "0-0"
	lowest = stock_data['low'][co-20]
	highest = stock_data['high'][co-20]
	r = range(co-20,co)
	for x in r:
		if lowest>stock_data['low'][x]:
			lowest = stock_data['low'][x]
		if highest<stock_data['high'][x]:
			highest = stock_data['high'][x]
	return str(lowest)+"-"+str(highest)

def getpercent(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_ewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_ewma.csv')
	co = stock_data['close'].count()
	if co<=1:
		return 0
	per = stock_data['percent'][co-1]*100
	return numpy.round(per,2)

def getJDZS(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_ewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_ewma.csv')
	co = stock_data['close'].count()
	if co<=30:
		return 0
	jd = stock_data['ejd'][co-1]
	jd0 = stock_data['ejd'][co-2]
	if (jd>0) and (jd0<0):
		return 1
	else:
		return 0

def getTiaoKong(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_ewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_ewma.csv')
	co = stock_data['close'].count()
	if co<=30:
		return 0
	lo = stock_data['low'][co-1]
	hi = stock_data['high'][co-2]
	if lo>hi:
		return 1
	else:
		return 0

def getLastDay(stockCode):
	pa = os.getcwd()
	if os.path.exists(pa+'/'+stockCode+'_ewma.csv')==False:
		return 0
	stock_data = pandas.read_csv(stockCode+'_ewma.csv')
	co = stock_data['close'].count()
	if co<1:
		return 0
	day = time.strftime('%d',time.localtime())
	if day[0]=='0':
		day = day[1:]
	mo = time.strftime('%m',time.localtime())
	if mo[0]=='0':
		mo = mo[1:]
	too = time.strftime('%Y',time.localtime())
	#today = too+"-"+mo+"-"+day
	today = sys.argv[1]
	if str(stock_data['date'][co-1])==today:
		return 1
	else:
		return 0


def getbasic(stockCode):
	stock_data = pandas.read_csv('d:/py/all.csv')
	i = 0
	idx = 0
	for x in stock_data['code']:
		if x==stockCode:
			idx =i
			break
		else:
			i += 1
	b = {}
	b['pe'] = stock_data['pe'][idx]
	b['pb'] = stock_data['pb'][idx]
	b['totals'] = stock_data['totals'][idx]
	b['reservedPerShare'] = stock_data['reservedPerShare'][idx]
	b['esp'] = stock_data['esp'][idx]
	b['bvps'] = stock_data['bvps'][idx]
	return b



#connect to mongodb
mongoserver = 'ds059644.mongolab.com'
port = 59644
dbname = 'jiucaidi'
dbuser = 'jiucaidi'
dbpass = 'jiucaidi1976'

too = time.strftime('%Y_%m_%d',time.localtime())
upinfo = time.strftime('%Y-%m-%d %H:%M',time.localtime())
client = pymongo.MongoClient('mongodb://jiucaidiowner:jiucaidi1976@ds059644.mongolab.com:59644/jiucaidi?authMechanism=SCRAM-SHA-1')
#client.jiucaidi.authenticate('jiucaidiowner','jiucaidi1976',mechanism='SCRAM-SHA-1')



#insert into stockinfo
'''
collections = client.jiucaidi.stockinfo
collections.remove()
collections.create_index("stcode")
collections.create_index("stname")
collections.create_index("stbelong")

stcode=[]
stname=[]
stbelong=[]

f=open('stname.txt','r')
for line in f.readlines():
	stname.append(line.strip())
f.close()

f=open('stcode.txt','r')
for line in f.readlines():
	stcode.append(line.strip())
f.close()

f=open('stbelong.txt','r')
for line in f.readlines():
	stbelong.append(line.strip())
f.close()

co=len(stcode)
plist = []
for x in range(0,co):
	p = {}
	p["stcode"]=stcode[x]
	p["stname"]=stname[x]
	p["stbelong"]=stbelong[x]
	plist.append(p)
collections.insert(plist)	
'''


#insert data to 
'''
stcode=[]
stname=[]
stbelong=[]
stgn=[]


f = codecs.open('stname.txt','r',encoding='utf-8')
for line in f.readlines():
	stname.append(line.strip())
f.close()

f= open('stcode2.txt','r')
for line in f.readlines():
	stcode.append(line.strip())
f.close()

f= codecs.open('stbelong.txt','r',encoding='utf-8')
for line in f.readlines():
	stbelong.append(line.strip())
f.close()

f= codecs.open('stgn.txt','r',encoding='utf-8')
for line in f.readlines():
	stgn.append(line.strip())
f.close()


collections = client.jiucaidi['everydaysh']
collections.remove()
collections.create_index("stcode")
collections.create_index("macd")
collections.create_index("kdj")
collections.create_index("macdback")
collections.create_index("kdjback")
collections.create_index("thirtydaysgrow")
collections.create_index("macdback")
collections.create_index("bollstd")#tu po boll up line, and mid up
collections.create_index("volume")
collections.create_index("rsi")
collections.create_index("chaobaoluo")
collections.create_index("realchaobaoluo")
collections.create_index("percent")

rssh=[]
rssz=[]
rscy=[]

fff = codecs.open('allstdata.json','r',encoding='utf-8')
sss = json.loads(fff.read())


i = 0
for x in sss:
	print x['stcode']
	reo = getLastDay(x['stcode'])
	if reo==0:
		continue
	p = {}

	#ba = getbasic(x)
	p['pe'] = x['pe']
	p['pb'] = x['pb']
	p['totals'] = x['totals']
	p['reservedPerShare']=x['reservedPerShare']
	p['outstanding']=x['outstanding']
	p['esp']=x['esp']
	p['bvps']=x['bvps']
	p['stcode']=x['stcode']
	p['stname']=x['stname']
	p['stbelong']=x['stbelong']
	p['stgn']=x['stgn']
	tcode = x['stcode']
	p['macd']=calcMACD(tcode)
	p['macdback']=calcMACDback(tcode)
	p['kdj']=calcKDJ(tcode)
	p['kdjback']=calcKDJback(tcode)
	p['volume']=chaoDi(tcode)
	p['chaobaoluo']=chaoBaoLuo(tcode)
	p['realchaobaoluo']=realChaoBaoLuo(tcode)
	p['rsi']=getRsi(tcode)
	p['thirtydaysgrow']=get30daysup(tcode)
	p['avghighlowdiff']=getAmpli(tcode)
	p['percent']=getpercent(tcode)
	p['bollstd']=getboll(tcode)
	p['bollstdsign']=getbollsign(tcode)
	p['spandpr']=getpressandsupport(tcode)
	p['ejd']=getJDZS(tcode)
	p['tiaokong']=getTiaoKong(tcode)

	if tcode.find('SH')>-1:
		print "add to sh[]"
		rssh.append(p)
	elif tcode.find('SZ0')>-1:
		print "add to sz[]"
		rssz.append(p)
	else:
		print "add to cy[]"
		rscy.append(p)	
	i += 1
'''

collections = client.jiucaidi['everydaysh']
collections.remove()
collections.create_index("stcode")
collections.create_index("macd")
collections.create_index("kdj")
collections.create_index("macdback")
collections.create_index("kdjback")
collections.create_index("thirtydaysgrow")
collections.create_index("macdback")
collections.create_index("bollstd")#tu po boll up line, and mid up
collections.create_index("volume")
collections.create_index("rsi")
collections.create_index("chaobaoluo")
collections.create_index("realchaobaoluo")
collections.create_index("percent")

print "insert sh data"
f = codecs.open('shdata.json','r',encoding='utf-8')
shdatas = json.loads(f.read())
collections.insert(shdatas)
f.close()

co2 = client.jiucaidi['everydaysz']
co2.remove()
co2.create_index("stcode")
co2.create_index("macd")
co2.create_index("kdj")
co2.create_index("macdback")
co2.create_index("kdjback")
co2.create_index("thirtydaysgrow")
co2.create_index("macdback")
co2.create_index("bollstd")#tu po boll up line, and mid up
co2.create_index("volume")
co2.create_index("rsi")
co2.create_index("chaobaoluo")
co2.create_index("realchaobaoluo")
co2.create_index("percent")

print "insert sz data"
f = codecs.open('szdata.json','r',encoding='utf-8')
szdatas = json.loads(f.read())
co2.insert(szdatas)
f.close()


co3 = client.jiucaidi['everydaycy']
co3.remove()
co3.create_index("stcode")
co3.create_index("macd")
co3.create_index("kdj")
co3.create_index("macdback")
co3.create_index("kdjback")
co3.create_index("thirtydaysgrow")
co3.create_index("macdback")
co3.create_index("bollstd")#tu po boll up line, and mid up
co3.create_index("volume")
co3.create_index("rsi")
co3.create_index("chaobaoluo")
co3.create_index("realchaobaoluo")
co3.create_index("percent")


print "insert cy data"
f = codecs.open('cydata.json','r',encoding='utf-8')
cydatas = json.loads(f.read())
co3.insert(cydatas)
f.close()




upinfo = time.strftime('%Y-%m-%d %H:%M',time.localtime())

collections2 = client.jiucaidi.updateinfo
collections2.remove()
collections2.insert({"table":"everyday","date":upinfo})




