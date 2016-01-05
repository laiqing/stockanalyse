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
import leancloud
from leancloud import Object
from leancloud import Query


class SHStockData(Object):	
	pass

class SZStockData(Object):
	pass

class CYStockData(Object):
	pass

class EveryDay(Object):
	pass


#get json file, insert into {{"everydaycy":[...]},{"everydaysh":[...]},{"everydaysz":[...]}}
#get everyday data , insert into {"2015-12-12":[...]}
leancloud.init('qazb7phh0uxqarjyd0agnbw7qwu65xff0e98sbbejfx8wyat', master_key='awfwb8rjhozpmmilpf7r339jx3qcjyuai7nqkk1qwfbnhu9x')

#remove old data

query = Query(SZStockData)
query.limit(1000)
objlist = query.find()
for x in objlist:
	#print x
	x.destroy()
print "sz remove 1000"

objlist = query.find()
query.limit(1000)
for x in objlist:
	x.destroy()

print "sz remove 2000"

query = Query(SHStockData)
query.limit(1000)
objlist = query.find()
for x in objlist:
	#print x
	x.destroy()

print "sh remove 1000"

objlist = query.find()
query.limit(1000)
for x in objlist:
	x.destroy()

print "sh remove 2000"

query = Query(CYStockData)
query.limit(1000)
objlist = query.find()
for x in objlist:
	#print x
	x.destroy()

print "cy remove 1000"

query = Query(EveryDay)
objlist = query.find()
for x in objlist:	
	x.destroy()





#cy.destroy()


f = codecs.open('cydata.json','r',encoding='utf-8')
datas = json.loads(f.read())



for x in datas:
	print 'insert:',x['stcode']		
	item = CYStockData()
	item.set('spandpr',x['spandpr'])
	item.set("kdj",x['kdj'])
	item.set("outstanding",x['outstanding'])
	item.set("gpjj",x['gpjj'])
	item.set("high",x['high'])
	item.set("open",x['open'])
	item.set("close",x['close'])
	item.set("low",x['low'])
	item.set("kdjback",x['kdjback'])
	item.set("macd",x['macd'])
	item.set("macdback",x['macdback'])
	item.set("stbelong",x['stbelong'])
	item.set("stgn",x['stgn'])
	item.set("stname",x['stname'])
	item.set("esp",x['esp'])
	item.set("ejd",x['ejd'])
	item.set("bollstd",x['bollstd'])
	item.set("bollstdsign",x['bollstdsign'])
	item.set("emalow",x['emalow'])
	item.set("percent",x['percent'])
	item.set("realchaobaoluo",x['realchaobaoluo'])
	item.set("totals",x['totals'])
	item.set("pb",x['pb'])
	item.set("pe",x['pe'])
	item.set("chaobaoluo",x['chaobaoluo'])
	item.set("rsi",x['rsi'])
	item.set("thirtydaysgrow",x['thirtydaysgrow'])
	item.set("volume",x['volume'])
	item.set("bollmidup",x['bollmidup'])
	item.set("stcode",x['stcode'])
	item.set("ema15per",x['ema15per'])
	item.set("reservedPerShare",x['reservedPerShare'])
	item.set("avghighlowdiff",x['avghighlowdiff'])
	item.set("tiaokong",x['tiaokong'])
	item.set("bvps",x['bvps'])	
	item.set("highbreakout",x['highbreakout'])
	item.save()
	
f.close()




f = codecs.open('szdata.json','r',encoding='utf-8')
szdatas = json.loads(f.read())
for x in szdatas:
	print 'insert:',x['stcode']
	item = SZStockData()
	item.set('spandpr',x['spandpr'])
	item.set("kdj",x['kdj'])
	item.set("outstanding",x['outstanding'])
	item.set("gpjj",x['gpjj'])
	item.set("high",x['high'])
	item.set("open",x['open'])
	item.set("close",x['close'])
	item.set("low",x['low'])
	item.set("kdjback",x['kdjback'])
	item.set("macd",x['macd'])
	item.set("macdback",x['macdback'])
	item.set("stbelong",x['stbelong'])
	item.set("stgn",x['stgn'])
	item.set("stname",x['stname'])
	item.set("esp",x['esp'])
	item.set("ejd",x['ejd'])
	item.set("bollstd",x['bollstd'])
	item.set("bollstdsign",x['bollstdsign'])
	item.set("emalow",x['emalow'])
	item.set("percent",x['percent'])
	item.set("realchaobaoluo",x['realchaobaoluo'])
	item.set("totals",x['totals'])
	item.set("pb",x['pb'])
	item.set("pe",x['pe'])
	item.set("chaobaoluo",x['chaobaoluo'])
	item.set("rsi",x['rsi'])
	item.set("thirtydaysgrow",x['thirtydaysgrow'])
	item.set("volume",x['volume'])
	item.set("bollmidup",x['bollmidup'])
	item.set("stcode",x['stcode'])
	item.set("ema15per",x['ema15per'])
	item.set("reservedPerShare",x['reservedPerShare'])
	item.set("avghighlowdiff",x['avghighlowdiff'])
	item.set("tiaokong",x['tiaokong'])
	item.set("bvps",x['bvps'])	
	item.set("highbreakout",x['highbreakout'])
	item.save()

f.close()


f = codecs.open('shdata.json','r',encoding='utf-8')
szdatas = json.loads(f.read())
for x in szdatas:
	print 'insert:',x['stcode']
	item = SHStockData()
	item.set('spandpr',x['spandpr'])
	item.set("kdj",x['kdj'])
	item.set("outstanding",x['outstanding'])
	item.set("gpjj",x['gpjj'])
	item.set("high",x['high'])
	item.set("open",x['open'])
	item.set("close",x['close'])
	item.set("low",x['low'])
	item.set("kdjback",x['kdjback'])
	item.set("macd",x['macd'])
	item.set("macdback",x['macdback'])
	item.set("stbelong",x['stbelong'])
	item.set("stgn",x['stgn'])
	item.set("stname",x['stname'])
	item.set("esp",x['esp'])
	item.set("ejd",x['ejd'])
	item.set("bollstd",x['bollstd'])
	item.set("bollstdsign",x['bollstdsign'])
	item.set("emalow",x['emalow'])
	item.set("percent",x['percent'])
	item.set("realchaobaoluo",x['realchaobaoluo'])
	item.set("totals",x['totals'])
	item.set("pb",x['pb'])
	item.set("pe",x['pe'])
	item.set("chaobaoluo",x['chaobaoluo'])
	item.set("rsi",x['rsi'])
	item.set("thirtydaysgrow",x['thirtydaysgrow'])
	item.set("volume",x['volume'])
	item.set("bollmidup",x['bollmidup'])
	item.set("stcode",x['stcode'])
	item.set("ema15per",x['ema15per'])
	item.set("reservedPerShare",x['reservedPerShare'])
	item.set("avghighlowdiff",x['avghighlowdiff'])
	item.set("tiaokong",x['tiaokong'])
	item.set("bvps",x['bvps'])	
	item.set("highbreakout",x['highbreakout'])
	item.save()

f.close()


upinfo = time.strftime('%Y-%m-%d %H:%M',time.localtime())
dd = EveryDay()
dd.set('date',upinfo)
dd.save()





	
