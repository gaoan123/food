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
import os
from dianping_check_dir import check_and_create_dir,get_trace_whole_dir

path = sys.path.append('..')
def scrap_all_menus(driver):
    url = 'https://www.dianping.com/'
    driver.get(url)
    time.sleep(5)
    page_content = driver.page_source
    doc = pq(page_content)
    menu_list = []
    for each_info in doc('.groups .sec-items'):
        for i in pq(each_info)('.second-item'):
            if pq(i).text() != '其他':
                print(pq(i).attr.href, pq(i).text())
                menu_list.append([pq(i).text(),pq(i).attr.href])
        break

    return menu_list

def scrap_all_menus_file(driver):
    filename = 'write_data.txt'
    #file_obj = open(filename, 'a+',encoding="utf-8")
    url = 'https://www.dianping.com/'
    driver.get(url)
    time.sleep(5)
    page_content = driver.page_source
    doc = pq(page_content)
    menu_list = []
    for each_info in doc('.groups .sec-items'):
        for i in pq(each_info)('.second-item'):
            if pq(i).text() != '其他':
                print(pq(i).attr.href, pq(i).text())
                with open(filename,'a+', encoding="utf-8") as f:
                    f.write(pq(i).text() + "\n")
                menu_list.append([pq(i).text(),pq(i).attr.href])
        break
    #file_obj.close()
    with open(filename,encoding="utf-8") as f:
        for line in f.readlines():
            print(line)
    return menu_list

def scrap_all_menus_Commercial_area(driver,city):
    url = 'https://www.dianping.com/' + city + '/food'
    #url = 'https://www.dianping.com/shanghai/food'
    trace_dir = get_trace_whole_dir()
    filename = city + '.txt'
    #if os.path.exists(filename) != True:
    filename = trace_dir + filename
    fp = open(filename, 'w')
    fp.close()
    driver.get(url)
    time.sleep(5)
    page_content = driver.page_source
    doc = pq(page_content)
    menu_list = []
    Commercial_area_list = []
    Commercial_area_food_urllist = []
    for each_info in doc('.f_pop_business .fpp_business .list > dt'):
        #print(each_info)
        #print(pq(each_info))
        area = pq(each_info)('a').text()
        area_url = 'https://www.dianping.com' + pq(each_info)('a').attr("href")
        print(area,area_url)

        Commercial_area_list.append([area,area_url])

    for each_area in Commercial_area_list:
        print('----------: ',each_area)
        driver.get(each_area[1])
        random.randint(3,6)
        page_content = driver.page_source
        doc = pq(page_content)
        for each_info in doc('.J_filter_category .nc-contain .nc-more > a'):
            print(pq(each_info))
            food_name = pq(each_info)('span').text()
            food_url = pq(each_info)('a').attr("href")
            if food_url.find('javascript:;') != -1:
                break
            Commercial_area_food_urllist.append([food_name,food_url])
            #print(each_area[0],food_name,food_url,len(Commercial_area_food_urllist))
            with open(filename, 'a+', encoding="utf-8") as f:
                f.write(each_area[0] + ' ' + food_name + ' ' + food_url + "\n")

    return Commercial_area_food_urllist

def scrap_all_Submenus_specify_district_when_exceed_max_page(driver,city,district,specify_food):
    detail_dir = check_and_create_dir(city,specify_food)
    url = 'https://www.dianping.com/' + city + '/food'
    #url = 'https://www.dianping.com/shanghai/food'
    filename = city + '_' + district + '_' +  specify_food + '_' + 'max_page' + '.txt'
    filename = detail_dir + filename
    #if os.path.exists(filename) != True:
    #    fp = open(filename, 'w')
    #    fp.close()
    #else:
    #    fp = open(filename, 'w')
    #    fp.close()
    fp = open(filename, 'w')
    fp.close()
    driver.get(url)
    time.sleep(3)
    page_content = driver.page_source
    doc = pq(page_content)
    menu_list = []
    Commercial_area_list = []
    Commercial_area_food_urllist = []
    for each_info in doc('.f_pop_business .fpp_business .list'):
        #print(each_info)
        #print(pq(each_info))
        #print('*' * 100)
        area = pq(each_info)('dt a').text()
        if area == district:
            for each_ie in pq(each_info)('dd a'):
                #print(each_ie)

                sub_district = pq(each_ie)('a').text()
                sub_district_url = 'https://www.dianping.com' + pq(each_ie)('a').attr('href')
                print(sub_district,sub_district_url)
                Commercial_area_list.append([area,sub_district,sub_district_url])
            break

    for each_area in Commercial_area_list:
        print('----------: ',each_area)
        driver.get(each_area[2])
        random.randint(3,6)
        page_content = driver.page_source
        doc = pq(page_content)
        for each_info in doc('.J_filter_category .nc-contain .nc-more > a'):
            #print(pq(each_info))
            food_name = pq(each_info)('span').text()
            print('----------------: ',food_name)
            if food_name == specify_food:
                print('food_name == specify_food')
                food_url = pq(each_info)('a').attr("href")
                if food_url.find('javascript:;') != -1:
                    break
                Commercial_area_food_urllist.append([each_area[0],food_name,food_url])
                #print(each_area[0],food_name,food_url,len(Commercial_area_food_urllist))
                with open(filename, 'a+', encoding="utf-8") as f:
                    f.write(each_area[0] + ' ' +food_name + ' ' + food_url + "\n")
                break

    return Commercial_area_food_urllist

#比如崇明火锅的url,不是崇明地区的，是上海整个火锅的url,check目的是避免重复
def check_if_valid_for_url(doc,district,specify_food):
    try:
        target_str = pq(doc('.J_bread span')[6])
        #print(pq(doc('.J_bread span')[6]))
        district_get = pq(target_str)('span a span').text()
        print(district)
        if district_get == district:
            print('check_if_valid_for_url valid: ',district)
            return True

    except:
        print('check_if_valid_for_url invalid: ', district)
        return False


def get_all_menus_specify_city_and_checkIf_exceed_max_page_not_include_url_exceed_50(driver,city,specify_food,menulist):
    #判断每个url是否超过点评给的最大页面50，如果超了，去掉这个url用子url代替
    dianping_max = 50
    exceed_index_list = []
    sub_menu_list = []
    menu_index = 0
    sub_list_len = 0
    for each_ie in menulist:
        driver.get(each_ie[2])
        page_content = driver.page_source
        doc = pq(page_content)
        time.sleep(2)

        result_check = check_if_valid_for_url(doc,each_ie[0],specify_food)
        if result_check == False:
            exceed_index_list.append(menu_index) #url 无效也要去掉
            continue
        max_page = 0
        # driver.find_element_by_css_selector('.page .next').click()
        for each_info in doc('.page .PageLink'):
            if int(pq(each_info).attr.title) > max_page:
                max_page = int(pq(each_info).attr.title)
        print('max_page: ', max_page)
        if max_page == dianping_max:
            print('city,specify_food,district exceed max page: ',city,specify_food,each_ie[0])
            district = each_ie[0]
            sub_list = scrap_all_Submenus_specify_district_when_exceed_max_page(driver,city,district,specify_food)
            sub_menu_list.append(sub_list)
            exceed_index_list.append(menu_index)
        menu_index = menu_index + 1

    exceed_index_list.sort(reverse=True)
    for each_index in exceed_index_list:
        menulist.pop(each_index)

    for each_sub in sub_menu_list:
        menulist = menulist + each_sub
        sub_list_len = sub_list_len + len(each_sub)
    detail_dir = check_and_create_dir(city, specify_food)
    filename = city + specify_food + '_combine_' + '.txt'
    filename = detail_dir + filename
    fp = open(filename, 'w')
    fp.close()
    for i in menulist:
        print(i)
        with open(filename, 'a+', encoding="utf-8") as f:
            f.write(i[0] + ' ' + i[1] + ' ' + i[2] + "\n")
    print('menulist sub_list len: ',len(menulist),sub_list_len)
    return menulist


def get_all_menus_specify_city_and_checkIf_exceed_max_page(driver,city,specify_food,menulist):
    #判断每个url是否超过点评给的最大页面50，如果超了，去掉这个url用子url代替
    dianping_max = 50
    exceed_index_list = []
    sub_menu_list = []
    menu_index = 0
    sub_list_len = 0
    tmp_urllist = []
   #menulist = []
   #delete_url = []
   #menu_counter = 0
   #for each_menu in input_menulist: #去除重复的url
   #    if each_menu[2] not in tmp_urllist:
   #        tmp_urllist.append(each_menu[2])
   #        menulist.append(each_menu)

   #for i in menulist:
   #    print('VVVVVVVVVVVVV: ',i)

    for each_ie in menulist:
        driver.get(each_ie[2])
        page_content = driver.page_source
        doc = pq(page_content)
        time.sleep(2)

        result_check = check_if_valid_for_url(doc,each_ie[0],specify_food)
        #if result_check == False:
        #    exceed_index_list.append(menu_index) #url 无效也要去掉
        #    continue

        max_page = 0
        # driver.find_element_by_css_selector('.page .next').click()
        for each_info in doc('.page .PageLink'):
            if int(pq(each_info).attr.title) > max_page:
                max_page = int(pq(each_info).attr.title)
        print('max_page: ', max_page)
        if max_page == dianping_max:
            print('city,specify_food,district exceed max page: ',city,specify_food,each_ie[0])
            district = each_ie[0]
            sub_list = scrap_all_Submenus_specify_district_when_exceed_max_page(driver,city,district,specify_food)
            sub_menu_list.append(sub_list)
            #exceed_index_list.append(menu_index)
        menu_index = menu_index + 1

    #exceed_index_list.sort(reverse=True)
    #for each_index in exceed_index_list:
    #    menulist.pop(each_index)

    for each_sub in sub_menu_list:
        menulist = menulist + each_sub
        sub_list_len = sub_list_len + len(each_sub)
    detail_dir = check_and_create_dir(city, specify_food)
    filename = city + specify_food + '_combine_' + '.txt'
    filename = detail_dir + filename
    fp = open(filename, 'w')
    fp.close()
    for i in menulist:
        print(i)
        with open(filename, 'a+', encoding="utf-8") as f:
            f.write(i[0] + ' ' + i[1] + ' ' + i[2] + "\n")
    print('menulist sub_list len: ',len(menulist),sub_list_len)
    return menulist


def read_scrap_all_menus_Commercial_area(filename):
    #filename = 'Commercial_area_food_urllist.txt'
    area_food_url = []
    with open(filename,encoding="utf-8") as f:
        for line in f.readlines():
            print('have_scraped_menu_list line: ',line)
            print(line.split(' ')[0],line.split(' ')[1],line.split(' ')[2])
            area = line.split(' ')[0]
            foodname = line.split(' ')[1]
            foodurl = line.split(' ')[2].split("\n")[0]
            area_food_url.append([area,foodname,foodurl])
    return area_food_url

import operator
def check_preserve_and_combie_file(city,specify_food):
    detail_dir = check_and_create_dir(city, specify_food)
    combine_filename = city + specify_food + '_combine_' + '.txt'
    preserved_file = city + '_' + specify_food + '_preserved.txt'

    combine_filename = detail_dir + combine_filename
    preserved_file = detail_dir + preserved_file

    preserved_list = []
    combine_list = []
    if os.path.exists(preserved_file) == True:
        preserved_list = read_scrap_all_menus_Commercial_area(preserved_file)

    if os.path.exists(combine_filename) == True:
        combine_list = read_scrap_all_menus_Commercial_area(combine_filename)
    cmp_result = False
    cmp_result = operator.eq(combine_list, preserved_list)
    print('combine_list,preserved_list,cmp_result: ',len(combine_list),len(preserved_list),cmp_result)
    if cmp_result == True:#
        print('two list equal,it return True')
    return cmp_result

def check_combie_file_if_exist(city,specify_food):
    detail_dir = check_and_create_dir(city, specify_food)
    combine_filename = city + specify_food + '_combine_' + '.txt'
    preserved_file = city + '_' + specify_food + '_preserved.txt'

    combine_filename = detail_dir + combine_filename
    preserved_file = detail_dir + preserved_file

    preserved_list = []
    combine_list = []
    if os.path.exists(preserved_file) == True:
        preserved_list = read_scrap_all_menus_Commercial_area(preserved_file)

    if os.path.exists(combine_filename) == True:
        combine_list = read_scrap_all_menus_Commercial_area(combine_filename)
        if len(combine_list) > 0:
            print('combine_filename is exist,and it neednt scrap urls again')
            return False

    return True



def read_specify_catagory_all_menus_Commercial_area(filename,specify_catagory):
    #filename = 'Commercial_area_food_urllist.txt'
    area_food_url = []
    with open(filename,encoding="utf-8") as f:
        for line in f.readlines():
            #print('have_scraped_menu_list line: ',line)
            #print(line.split(' ')[0],line.split(' ')[1],line.split(' ')[2])
            area = line.split(' ')[0]
            foodname = line.split(' ')[1]
            foodurl = line.split(' ')[2].split("\n")[0]
            if foodname == specify_catagory:
                print([area,foodname,foodurl])
                print('*' * 100)
                area_food_url.append([area,foodname,foodurl])
    return area_food_url

#if __name__ == '__main__':
#    url = 'https://www.dianping.com/'
#    cycle_counter = 0
#    dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置useragent
#    # dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0')  #根据需要设置具体的浏览器信息
#    dcap['phantomjs.page.settings.userAgent'] = (
#    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')  # 根据需要设置具体的浏览器信息
#    dcap['phantomjs.page.settings.loadImages'] = False
#    #driver = webdriver.PhantomJS(desired_capabilities=dcap)  # 封装浏览器信息
#    #menu = scrap_all_menus_file(driver)
#    menu_list = []
#    filename = 'write_data.txt'
#    have_scraped_menu_list =[]
#    preserved_file = 'preserved_file.txt'
#    with open(filename,encoding="utf-8") as f:
#        for line in f.readlines():
#            print(line)
#            menu_list.append(line)
#        print('menu_list: ',menu_list)
#
#    with open(preserved_file, encoding="utf-8") as f:
#        for line in f.readlines():
#            print('have_scraped_menu_list line: ', line)
#            have_scraped_menu_list.append(line)
#        print(have_scraped_menu_list)
#    #driver.close()

if __name__ == '__main__':
    url = 'https://www.dianping.com/'
    cycle_counter = 0
    dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置useragent
    # dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0')  #根据需要设置具体的浏览器信息
    dcap['phantomjs.page.settings.userAgent'] = (
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')  # 根据需要设置具体的浏览器信息
    dcap['phantomjs.page.settings.loadImages'] = False
    #driver = webdriver.PhantomJS(desired_capabilities=dcap)  # 封装浏览器信息
    city = 'nanjing'
    district = '松江区'
    specify_food = '火锅'

    #scrap_all_Submenus_specify_district_when_exceed_max_page(driver,city,district,specify_food)
    #read_scrap_all_menus_Commercial_area()


    #scrap_all_menus_Commercial_area(driver,city)
    #filename = city + '.txt'
    #debug_menu = []
    #menu_list = read_specify_catagory_all_menus_Commercial_area(filename, specify_food)
    #for i in menu_list:
    #    print('==============: ',i)
#
    #preserved_file = city + '_' + specify_food + '_preserved.txt'
    #fp = open(preserved_file, 'w')
    #fp.close()
    #have_scraped_menu_list = read_scrap_all_menus_Commercial_area(preserved_file)
    #for i in menu_list:
    #    if i not in have_scraped_menu_list:
    #        debug_menu.append(i)
    #print('---------------debug_menu : ',len(menu_list))
    #all_menu_list = get_all_menus_specify_city_and_checkIf_exceed_max_page(driver, city, specify_food, debug_menu)
#

    #url = 'http://www.dianping.com/shanghai/ch10/g110r5937'
    #driver.get(url)
    #page_content = driver.page_source
    #doc = pq(page_content)
    #time.sleep(2)
    #check_if_valid_for_url(doc,district,specify_food)
    specify_food = '火锅'
    city = 'shenzhen'
    check_preserve_and_combie_file(city,specify_food)