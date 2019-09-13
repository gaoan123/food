from math import sin, asin, cos, radians, fabs, sqrt
import xlrd
import xlwt
from datetime import date,datetime
import pandas as pd
import json
from urllib.request import urlopen, quote
import csv
import traceback
import os
import requests
from bs4 import BeautifulSoup
import traceback
# 异常处理
import xlwt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
import datetime
import re
#import lxml
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException,StaleElementReferenceException
from pyquery import PyQuery as pq
import urllib.request
#import xlwt
#from xlwt import *
#from relatedinfo_of_prodution import *
from time import ctime,sleep
from multiprocessing import Pool
import multiprocessing
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType

import random
import requests
#冷轧热轧等后面的一丢子集的链接能解析出来
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pymysql
import sys
from bs4 import BeautifulSoup
from time import ctime,sleep
from multiprocessing import Pool
import multiprocessing
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
import urllib.request
import random
import requests
#冷轧热轧等后面的一丢子集的链接能解析出来
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pymysql
import sys
path = sys.path.append('..')
#from Manager.ProxyManager import ProxyManager
#from DB.SsdbClient import SsdbClient
#from Util.LogHandler import LogHandler
EARTH_RADIUS = 6371  # 地球平均半径，6371km

def check_proxy():
    db = SsdbClient('db_time', '127.0.0.1', 6379, db=1)
    db.changeTable('db_time')
    dict_from_db_time = db.getAll()
    sort_ip_list = []
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    for key, value in dict_from_db_time.items():  # 新抓取的和库里已有的合并排序
        sort_ip_list.append(key)
    for ele in sort_ip_list:
        print(ele)
        try_num = 0
        while try_num < 5:
            try:
                proxy_support = urllib.request.ProxyHandler({'http': ele})
                opener = urllib.request.build_opener(proxy_support)
                urllib.request.install_opener(opener)
                a = urllib.request.urlopen("http://httpbin.org/ip").read().decode("utf8")
                print('----------------------:',a)
                break
            except:
                try_num = try_num + 1
                print('get lng lat try num:',try_num,ele)
        break


def hav(theta):
    s = sin(theta / 2)
    return s * s

def getlnglat(address):
    url = 'http://api.map.baidu.com/geocoder/v2/?address='
    output = 'json'
    ak = 'o0FyAazlrGYF1wuNKId9ljvdXlEtzRaf'#需填入自己申请应用后生成的ak
    add = quote(address)  # 本文城市变量为中文，为防止乱码，先用quote进行编码
    url2 = url + add + '&output=' + output + "&ak=" + ak
    req = urlopen(url2)

    res = req.read().decode()
    temp = json.loads(res)
    return temp

def get_distance_hav(lng0,lat0, lng1,lat1):
    "用haversine公式计算球面两点间的距离。"
    # 经纬度转换成弧度
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)

    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))
    #print(distance,type(distance))
    sdistance = str(distance)
    sdistance_dest = sdistance.split('.')[0] + '.' + sdistance.split('.')[1][0]
    return float(sdistance_dest)

def calc_distance_km_between_two_address(address1,address2):
    print('target address: ',address2)
    fail_num = 0
    distance_km = 0.0
    while fail_num < 5:
        try:
            lng0 = getlnglat(address1)['result']['location']['lng']  # 获取经度
            lat0 = getlnglat(address1)['result']['location']['lat']  # 获取纬度
            #print(lng0,lat0)
            lng1 = getlnglat(address2)['result']['location']['lng']  # 获取经度
            lat1 = getlnglat(address2)['result']['location']['lat']  # 获取纬度
            #print(lng1,lat1)
            distance_km = get_distance_hav(lng0, lat0, lng1, lat1)
            break
        except:
            fail_num = fail_num + 1
            print('get lng lat fail: ', fail_num)
    print(distance_km)
    return distance_km

#calc_distance_km_between_two_address('上海市宝山区呼玛路623号','上海市临沂路140号百联商场3楼')
#check_proxy()
a = [1,2,3,4,5]
b = [1,2,7,8,9]
for i in a:
    if i not in b:
        print(i)




