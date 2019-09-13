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






url = 'http://www.dianping.com/shanghai/ch10/g110'
dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置useragent
dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0')  #根据需要设置具体的浏览器信息
#dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')  # 根据需要设置具体的浏览器信息
dcap['phantomjs.page.settings.loadImages'] = False
driver = webdriver.PhantomJS(desired_capabilities=dcap)  # 封装浏览器信息
print(type(driver))
driver.get(url)
time.sleep(8)
a = driver.find_element_by_id("shap-all-list")
print(a)








# 写入xls表
# Cookie记录登录信息，session请求
def get_content(url, headers=None, proxy=None):
    html = requests.get(url, headers=headers).content
    return html


def get_url(html):
    soup = BeautifulSoup(html, 'lxml')

    shop_url_list = soup.find_all('div', class_='tit')
    # class是关键字，所以不能直接用，class_就可以了
    # print (shop_url_list)
    # find是只查询一次，find_all()是查询多次返回一个列表，如果没有值就返回空
    # 列表推导式
    return [i.find('a')['href'] for i in shop_url_list]


def get_detail_content(html):
    try:
        soup = BeautifulSoup(html, 'lxml')
        price = soup.find('span', id='avgPriceTitle').text
        evaluation = soup.find('span', id='comment_score').find_all('span', class_='item')
        # 提取第一个span里面的title属性
        the_star = soup.find('div', class_='brief-info').find('span')['title']
        comments = soup.find('span', id="reviewCount").text
        title = soup.find('div', class_='breadcrumb').find('span').text
        address = soup.find('span', itemprop="street-address")['title']
        # u的意思是代表unicode编码
        print(u'店名:' + title)
        for i in evaluation:
            print(i.text)
        print(price)
        print(u'评价数量:' + comments)
        print(u'地址:' + address.strip())
        print(u'评价星级:' + the_star)
        print('===========================')
        return (title, evaluation[0].text, evaluation[1].text, evaluation[2].text, price, comments, address, the_star)
    except:
        traceback.print_exc()


if __name__ == '__main__':

    items = []
    all_url = []

    fk_url = []
    # 将所有商户的评论url全都打印出
    for i in range(0, 5):
        start_url = 'https://www.dianping.com/search/category/344/10/p' + str(i)
        print(start_url)
        all_url.append(start_url)

    base_url = 'https://www.dianping.com/'
    # 表头
    # 如果不设置cookie有可能导致出现403错误，禁止访问
    headers = {
        'User-Agent': 'Mozilla/5.0(Windows NT 6.1; WOW64) AppleWebkit'

                      'Cookie' '_lxsdk_cuid = 15c862ce29774 - 0e90b90a55f72 - 414a0229 - 1fa400 - 15c862ce299c8;_lxsdk = 15c862ce29774 - 0e90b90a55f72 - 414a0229 - 1fa400 - 15c862ce299c8;_hc.v = 77b1169f - 1763 - c5b6 - ade2 - a81093a8b4cd.1496899708;PHOENIX_ID = 0a010725 - 15c862cf0e2 - 207bfe7;JSESSIONID = 6AEA99FE3A5B0BF2920C833821F8D711;aburl = 1;cy = 344;cye = changsha;_lxsdk_s = 15c862ce29c - ce2 - f25 - 8c % 7C % 7C84;__mta = 219083046.1496899711367.1496902358445.1496902376486.8'

    }
    # 把多个列表里的url里面的url存储到一个列表里去，便于查询数据
    for url in all_url:
        start_html = get_content(url)
        print(start_html)
        durl = get_url(start_html)
        for i in durl:
            print('---------------: ',i)
            fk_url.append(i)
            print(i)

    # 列表推导式
    # base_url+url打印完整url
    url_list = [base_url + url for url in fk_url]

    for i in url_list:
        detail_html = get_content(i)
        item = get_detail_content(detail_html)
        items.append(item)

    newTable = 'DZDPdemo1.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('test1')
    headData = ['商户名字', '口味评分', '环境评分', '服务评分', '人均价格', '评论数量', '地址', '商户星级']
    for column in range(0, 8):
        # 0把行定位到第一行了列 后面是设置字体
        ws.write(0, column, headData[column], xlwt.easyxf('font:bold on'))

    index = 1

    lens = len(items)
    print(u'数据总长度=' + str(lens))
    # 有多少数据
    # 只对列做了一个for循环，因为行列都要写入，所以做两个for循环
    # 多少行由列表数据决定的，有多少数据就有多少行
    # index代表的是行，我们从1开始是因为标题已经占据了第一行
    # 对list做了两次索引，第一次是商户信息拿出来，第二个索引是把商户的详细信息拿出来
    # 简单的来说，j就代表一个商户，i[0]相当于代表店名，i[1]相当于代表evaluation[0].text依次类推
    for j in range(0, lens):
        for i in range(0, 8):
            ws.write(index, i, items[j][i])
        index += 1
    wb.save(newTable)
