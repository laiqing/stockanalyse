#encoding:utf-8 

import urllib,urllib2
import httplib
import shutil
import os
import re
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

#vip.stock.finance.sina.com.cn

#json_v2.php

def getLow(srcstr):	
	reg = re.compile(r'low:"[0-9]*\.[0-9]*",')
	match = re.search(reg, srcstr)
	if match:
		result = match.group(0)
		xx = result[5:-2]
		return float(xx)
	else:
		return 0

def getOpen(srcstr):
	reg = re.compile(r'open:"[0-9]*\.[0-9]*",')
	match = re.search(reg, srcstr)
	if match:
		result = match.group(0)
		xx = result[6:-2]
		return float(xx)
	else:
		return 0

url="http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?num=3000&sort=changepercent&asc=0&node=hs_a&symbol=&_s_r_a=page&page=1"

crawlHeader = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'}	

cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
urllib2.install_opener(opener)
req = urllib2.Request(url,None,crawlHeader)
req.add_header("Accept","*/*")
req.add_header("Accept-Language", "*")
req.add_header("Connection", "keep-alive")
req.add_header("Cache-Control","no-cache")
req.add_header("Host","vip.stock.finance.sina.com.cn")
resp = urllib2.urlopen(req)
#print resp.getcode()
text = resp.read()
#print d
arr = text.split("},")

for x in arr:
	stidx = x.find("symbol:\"")
	code = x[stidx+8:stidx+16]
	low = getLow(x)
	print code,low

#for x in js:
#	print js

