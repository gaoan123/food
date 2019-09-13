import requests
from bs4 import BeautifulSoup
import traceback
import os
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
import pickle
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
from datetime import datetime
import random
import requests
#冷轧热轧等后面的一丢子集的链接能解析出来
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pymysql
import sys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
path = sys.path.append('..')
#from Manager.ProxyManager import ProxyManager
#from DB.SsdbClient import SsdbClient
#from Util.LogHandler import LogHandler
from distance_two_point import calc_distance_km_between_two_address
from decode_encrypted_stream import css_get_for_shoplist,decode_for_input_encrypted_stream
from decode_encrypted_stream import decode_score_for_service_taste_env_price
from scrap_all_menus import read_scrap_all_menus_Commercial_area,read_specify_catagory_all_menus_Commercial_area,get_all_menus_specify_city_and_checkIf_exceed_max_page,scrap_all_menus_Commercial_area,check_combie_file_if_exist
from input_check_code import readDianPingCookies
from dianping_check_dir import check_and_create_dir,get_trace_whole_dir
def convert(s):
    s = s.strip('&#x;') # 把'&#x957f;'变成'957f'
    s = bytes(r'\u' + s, 'ascii') # 把'957f'转换成b'\\u957f'
    return s.decode('unicode_escape') # 调用bytes对象的decode，encoding用unicode_escape，把b'\\u957f'从unicode转义编码解码成unicode的'长'。具体参见codecs的文档




dict_svg_text={}
list_svg_y=[]
dict_css_x_y={}


#a = doc('.shap-all-list')
all_shops = []
class cShopInfo(object):
    def __init__(self):
        self.address_info = ''
        self.shop_mainRegionName = ''
        self.shop_name = ''
        self.shop_id = ''
        self.shop_url = ''
        self.shop_city = ''
        self.shop_district = ''
        self.shop_star = ''
        self.shop_catagory = ''  # 菜系
        self.shop_subcatagory = ''
        self.taste_score = ''
        self.environment_score = ''
        self.service_score = ''
        self.avgPrice = ''
        self.recommend_foodlist = []
        self.distance_km = '' #距离目标点的距离
        self.cur_index = 0 #debug insert db except

def get_Shop_Info(driver,shop_catagory,happen_except,cur_index,shoplist_or_eachShop,city,shop_district):
    global all_shops
    global dict_svg_text
    global list_svg_y
    global dict_css_x_y
    code_city = {'beijing':'北京市','shanghai':'上海市','nanjing':'南京市','chengdu':'成都市','chongqing':'重庆市','wuhan':'武汉','shenzhen':'深圳市','wuxi':'无锡市','changsha':'长沙市','hangzhou':'杭州市'}
    shop_info = cShopInfo()
    page_content = driver.page_source
    #print('+++++==================: ',page_content)
    doc = pq(page_content)
    a = doc('.content-wrap #shop-all-list li')
    #print('debug 0')
    counter_shop = 1
    for i in a:
        print('*********************** begin cur page,cur shop: ',cur_index,counter_shop)
        have_the_same_shop = False
        shop_info = cShopInfo()
        #shop_name = pq(i)('.txt .tit a').text()
        #print(shop_name)
        shop_url = pq(i)('.txt .tit a').attr.href
        print('debug 2')
        #print('shop_url: ',shop_url)
        shop_addr = pq(i)('.operate .o-map')
        #print(re.sub(r'&#x....;',lambda match: convert(match.group()),str(shop_addr)))
        convert_str = re.sub(r'&#x....;',lambda match: convert(match.group()),str(shop_addr))
        print('debug 3')
        city_prefix = code_city[city]
        shop_info.shop_city = city_prefix
        shop_info.shop_district = shop_district
        print('shop city and shop_district: ',shop_info.shop_city,shop_info.shop_district)
        addr_info = city_prefix+ pq(convert_str).attr("data-address")
        shop_name = pq(convert_str).attr("data-sname")
        print(shop_name,addr_info,shop_url)
        shop_info.cur_index = cur_index
        if len(addr_info) > 63:
            addr_info = addr_info[0:63]
        shop_info.address_info = addr_info
        shop_info.shop_name = shop_name
        shop_info.shop_url = shop_url
        shop_info.shop_catagory = shop_catagory

        star_encode = pq(i)('.txt .sml-rank-stars').attr('title')
        star_convert_str = re.sub(r'&#x....;', lambda match: convert(match.group()), str(star_encode))
        shop_info.shop_star = star_convert_str
        print('get shop star score: ', star_convert_str)
        #print('main dict_svg_text: ',dict_svg_text)
        #print('main list_svg_y: ', list_svg_y)
        #print('main dict_css_x_y: ', dict_css_x_y)

        for sub in pq(i)('.tag-addr .tag'):
            #print('sub: ',pq(sub)('.tag > span'))
            if shop_info.shop_subcatagory == '':
                print('pq(sub)(.tag > span) shop_subcatagory: ',pq(sub)('.tag > span'))
                #shop_info.shop_subcatagory = decode_for_input_encrypted_stream(pq(sub)('.tag > span'), dict_svg_text, list_svg_y, dict_css_x_y,shoplist_or_eachShop)

                #shop_info.shop_subcatagory = decode_for_input_encrypted_stream(pq(sub)('.tag'), dict_svg_text,list_svg_y, dict_css_x_y,shoplist_or_eachShop)
                shop_info.shop_subcatagory = ''
            else:
                print('pq(sub).text() 1: ',sub)
                print('pq(sub).text() 2: ', pq(sub))
                decode_mainRegionName = False
                for y in pq(sub)('span'):
                    print('every class: ',pq(y).attr('class'))
                    if pq(y).attr('class') != 'tag':
                        decode_mainRegionName = True
                        break

                if decode_mainRegionName == True:
                    #shop_info.shop_mainRegionName = decode_for_input_encrypted_stream(pq(sub)('.tag > span'), dict_svg_text, list_svg_y, dict_css_x_y,shoplist_or_eachShop)

                    #shop_info.shop_mainRegionName = decode_for_input_encrypted_stream(pq(sub)('.tag'),dict_svg_text, list_svg_y,dict_css_x_y,shoplist_or_eachShop)
                    shop_info.shop_mainRegionName = ''
                else:
                    print('shop_mainRegionName no need decode')

                    #shop_info.shop_mainRegionName = pq(sub).text()
                    shop_info.shop_mainRegionName = ''


        print('shop_mainRegionName,shop_subcatagory: ',shop_info.shop_mainRegionName,shop_info.shop_subcatagory)

        decode_score_for_service_taste_env_price(shop_info,pq(i)('.txt .comment-list b span'),0)
        print('taste,service,enviroment: ',shop_info.taste_score,shop_info.service_score,shop_info.environment_score)

        recommend_food_list = pq(i)('.txt .recommend a')
        for each_food in recommend_food_list:
            print('each_food: ',pq(each_food).text())
            shop_info.recommend_foodlist.append(pq(each_food).text())
        print('recommend_foodlist: ',shop_info.recommend_foodlist)
        #shop_info.shop_star = star_convert_str
        #print('get shop star score: ', star_convert_str)

        #shop_id = pq(i)('.txt .tit a')[0].attr('data-shopid')
        shop_id = pq(pq(i)('.txt .tit a')[0]).attr('data-shopid')
        print('shop_id: ',shop_id,type(shop_id))
        shop_info.shop_id = shop_id

        #print('price: ',pq(i)('.txt .comment .mean-price b'))
        decode_score_for_service_taste_env_price(shop_info, pq(i)('.txt .comment .mean-price b'),1)
        print('avgPrice: ', shop_info.avgPrice)

        #shop_info.distance_km = calc_distance_km_between_two_address('上海市宝山区呼玛路623号', addr_info)
        shop_info.distance_km = '0'


        #if happen_except == True:
        #    for each in all_shops:
        #        if shop_info.shop_name == each.shop_name and shop_info.address_info == each.address_info:
        #            have_the_same_shop = True
        #            break
        #    if have_the_same_shop == False:
        #        all_shops.append(shop_info)
        #        have_the_same_shop = False
        #else:
        #    all_shops.append(shop_info)
        all_shops.append(shop_info)


        print('*********************** end cur page,cur shop: ', cur_index, counter_shop)
        counter_shop = counter_shop + 1
def sort_list_use_distance():
    db = pymysql.connect(host="127.0.0.1", user="root", passwd='axw19851111', db="can_yin_shop", charset="utf8")
    cursor = db.cursor()
    cursor.execute('select * from shop_info')
    scrap_tuple = cursor.fetchall()
    scrap_list = []
    for each_ele in scrap_tuple:
        scrap_tmp = list(each_ele)
        del scrap_tmp[0]
        print(scrap_tmp)
        scrap_list.append(scrap_tmp)
    print('scrap_list len:', len(scrap_list))
    sort_distance_list = []
    while len(scrap_list) > 0:
        minest_distance = 30000
        minest_index = 0
        counter = 0
        int_distance = 0
        for each_shop in scrap_list:
            int_distance = int(each_shop[3].split('.')[0]) * 10 + int(each_shop[3].split('.')[1])
            print('int_distance: ', int_distance)
            if int_distance <= minest_distance:
                minest_distance = int_distance
                minest_index = counter
            counter = counter + 1

        sort_distance_list.append(scrap_list[minest_index])
        scrap_list.remove(scrap_list[minest_index])
    print('***************************************************')
    print('sort_distance_list: ', len(sort_distance_list))
    cursor.execute('truncate table shop_info')
    db.commit()

    for each in sort_distance_list:
        try:
            sta = cursor.execute(
                'insert into shop_info (shop_name,address_info,shop_url,distance_km) values("%s","%s","%s","%s")'
                % (each[0], each[1], each[2], each[3]))
            if sta == 1:
                print('insert into shop_info success', each[0], each[1], each[2], each[3])
            else:
                print('insert into shop_info fail', each[0], each[1], each[2], each[3])
            db.commit()
        except:
            print('insert into shop_info except', each[0], each[1], each[2], each[3])
    db.commit()
    db.close()

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

def get_brower_driver_PHANTOMJS():
    dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置useragent
    # dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0')  #根据需要设置具体的浏览器信息
    dcap['phantomjs.page.settings.userAgent'] = (
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')  # 根据需要设置具体的浏览器信息
    dcap['phantomjs.page.settings.loadImages'] = False
    driver = webdriver.PhantomJS(desired_capabilities=dcap)  # 封装浏览器信息
    return driver



def get_brower_driver_fireFox():
    options = webdriver.FirefoxOptions()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
    profile = FirefoxProfile()
    profile.set_preference("general.useragent.override", user_agent)

    options.add_argument('-headless')
    driver  = webdriver.Firefox(profile,options=options)
    return driver
def get_brower_driver():
    options = webdriver.FirefoxOptions()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
    profile = FirefoxProfile()
    profile.set_preference("general.useragent.override", user_agent)

    options.add_argument('-headless')
    driver  = webdriver.Firefox(profile,options=options)

    tbCookies = readDianPingCookies()
    driver.get("http://www.dianping.com/")
    #brower.find_element_by_css_selector('.opt-btn.login').click()

    driver.implicitly_wait(1)  # 进行页面跳转或弹窗时需要设置等待时间，该句必不可少，不然就会定位不到弹窗或者新的页面内的元素
    #brower.find_element_by_class_name('bottom-password-login').click()

    for cookie in tbCookies:
        print('cookie,tbCookies[cookie]: ',cookie,tbCookies[cookie])
        driver.add_cookie({ "domain":"www.dianping.com",
                            "name":cookie,
                            "value":tbCookies[cookie],
                            "path":'/',
                            "expires":None })
    driver.get("http://www.dianping.com/")
    time.sleep(1)
    #print('---------------: ',driver.page_source)
    return driver



def get_brower_driver_ip(): #代理IP
    API_IP = "http://api.ip.data5u.com/dynamic/get.html?order=c007b0a31807fe965aff945c2d528403&sep=3"
    ip_str = requests.get(API_IP).content.decode()
    print('-----------------: ', ip_str)
    ip = ip_str.split(':')[0]
    port = ip_str.split(':')[1]
    print("ip,port: ",ip,port)
    profile = FirefoxProfile()
    # 激活手动代理配置（对应着在 profile（配置文件）中设置首选项）
    profile.set_preference("network.proxy.type", 1)
    # ip及其端口号配置为 http 协议代理
    profile.set_preference("network.proxy.http", ip)
    profile.set_preference("network.proxy.http_port", int(port))
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
    profile.set_preference("general.useragent.override", user_agent)

    # 所有协议共用一种 ip 及端口，如果单独配置，不必设置该项，因为其默认为 False
    profile.set_preference("network.proxy.share_proxy_settings", True)
    # 默认本地地址（localhost）不使用代理，如果有些域名在访问时不想使用代理可以使用类似下面的参数设置
    # profile.set_preference("network.proxy.no_proxies_on", "localhost")

    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    driver = webdriver.Firefox(profile, options=options)
    #driver.get('http://httpbin.org/ip')
    #print(driver.page_source)
    return driver

if __name__ == '__main__':
    url = 'http://www.dianping.com/shanghai/ch10/g110'
    cycle_counter = 0
    except_list = []
    preserved_shop_list = ['火锅','本帮江浙菜','日本菜', '面包甜点','咖啡厅','自助餐', '小吃快餐','西餐','韩国料理','粤菜','烧烤','川菜','素菜','东南亚菜','东北菜','湘菜','云南菜']
    #scrap_citylist = ['shanghai','beijing','nanjing','chengdu','chongqing','wuhan','shenzhen']
    #scrap_citylist = ['shanghai','beijing','chengdu','chongqing','wuxi']
    scrap_citylist = ['shanghai','beijing','shenzhen','nanjing','chengdu','wuhan','wuxi','changsha','chongqing','hangzhou']#火锅
    #scrap_citylist = ['shanghai', 'beijing', 'shenzhen', 'nanjing', 'chengdu', 'wuhan', 'wuxi', 'changsha','hangzhou']
    #driver = get_brower_driver()
    #filename = 'Commercial_area_food_urllist.txt'
    ongoing_scraped_list = []

    trace_dir = get_trace_whole_dir()
    driver = get_brower_driver()
    all_menu_list = []
    #food_list = ['创意菜','韩国料理']
    #food_list = ['面馆', '粉面馆','粥粉面']
    food_list = ['日本菜','自助餐']
    for each_cycle_food in food_list:
        for each_city in scrap_citylist:
            specify_food = each_cycle_food
            city = each_city
            print('the city : ',city,specify_food)
            check_scrap = check_combie_file_if_exist(city,specify_food)
            debug_menu = []
            detail_dir = check_and_create_dir(city,specify_food)
            combine_filename = city + specify_food + '_combine_' + '.txt'
            combine_filename = detail_dir + combine_filename
            if check_scrap == True:
                scrap_all_menus_Commercial_area(driver, city)
                filename = city + '.txt'
                filename = trace_dir + filename
                menu_list = read_specify_catagory_all_menus_Commercial_area(filename, specify_food)

                get_all_menus_specify_city_and_checkIf_exceed_max_page(driver, city, specify_food, menu_list)

                all_menu_list = read_scrap_all_menus_Commercial_area(combine_filename)
                for i in all_menu_list:
                    print('==============: ', i)
            else:
                all_menu_list = read_scrap_all_menus_Commercial_area(combine_filename)
                for i in all_menu_list:
                    print('==============: ', i)

            preserved_file = city + '_' + specify_food + '_preserved.txt'
            preserved_file = detail_dir + preserved_file
            if os.path.exists(preserved_file) != True:
                fp = open(preserved_file, 'w')
                fp.close()
            have_scraped_menu_list = []
            have_scraped_menu_list = read_scrap_all_menus_Commercial_area(preserved_file)
            for i in all_menu_list:
                if i not in have_scraped_menu_list:
                    debug_menu.append(i)

            file_except = city + '_' + specify_food + '_except.txt'
            file_except = detail_dir + file_except
            if os.path.exists(file_except) != True:
                fp = open(file_except, 'w')
                fp.close()

            preserved_file = city + '_' + specify_food + '_preserved.txt'
            preserved_file = detail_dir + preserved_file
            if os.path.exists(preserved_file) != True:
                fp = open(preserved_file, 'w')
                fp.close()

            #debug_menu = [['溧水区','烧烤','http://www.dianping.com/nanjing/ch10/g508r27661']]
            print('ongoing debug_menu: ',len(debug_menu))
            for each_url in debug_menu:
            #for each_url in menu_list:
                except_fail_num = 0
                write_to_db = False
                happen_except = False
                insert_page = 0
                url_get_error = False
                shop_catagory = each_url[1]
                shoplist_or_eachShop = False
                while except_fail_num < 3:
                    try:
                        max_page = 0
                        update_max_page = 0
                        cur_page = 0
                        except_list = []
                        #if happen_except == False:
                        #    all_shops = []

                        all_shops = []

                        #driver = get_brower_driver()
                        #time.sleep(random.randint(2,5))
                        if each_url in ongoing_scraped_list:
                            print('have the same url,please ignore it')
                            break
                        driver.get(each_url[2])
                        time.sleep(0.5)
                        doc = pq(driver.page_source)

                        #dict_css_x_y  ------ {'dp8dn': ('-588.0', '-1067.0', 49, '-1067.0'), 'dppla': ('-84.0', '-1394.0', 7, '-1394.0')}

                        #try:
                        #    dict_svg_text, list_svg_y, dict_css_x_y,shoplist_or_eachShop= css_get_for_shoplist(doc)
                        #except:
                        #    print('css_get_for_shoplist(doc) except')
                        #    time.sleep(1)
                        #    continue


                        print('current shop catagory: ',each_url[0],shop_catagory,each_url[2])
                        #time.sleep(5)
                        page_content = driver.page_source
                        doc = pq(page_content)
                        #driver.find_element_by_css_selector('.page .next').click()
                        for each_info in doc('.page .PageLink'):
                            if int(pq(each_info).attr.title) > max_page:
                                max_page = int(pq(each_info).attr.title)
                        print('max_page: ',max_page)
                        start_time = datetime.now()
                        #print('-------------------: ',page_content)

                        get_Shop_Info(driver,shop_catagory,happen_except,cur_page,shoplist_or_eachShop,city,each_url[0])
                        if max_page != 0:
                            cur_page = int(doc('.page .cur').text())
                            print('cur_page: ', cur_page, shop_catagory)
                            refresh_counter = 0
                            while cur_page < max_page:
                                try:
                                    driver.find_element_by_css_selector('.page .next').click()
                                except:
                                    if refresh_counter < 3:
                                        driver.refresh()
                                        refresh_counter = refresh_counter + 1
                                        time.sleep(1)
                                        continue
                                    else:
                                        record_info = 'driver.find_element_by_css_selector(.page .next).click()： '+ each_url[2]
                                        with open(file_except, 'a+', encoding="utf-8") as f:
                                            f.write('')
                                        url_get_error = True
                                        break


                                #time.sleep(random.randint(5, 10))
                                time.sleep(random.randint(1, 5))
                                page_content = driver.page_source
                                doc = pq(page_content)

                                print('+++++++++++++++++++++: ',str(doc('.content-wrap .pic-content .not-found-right')).find('没有找到'))
                                if str(doc('.content-wrap .pic-content .not-found-right')).find('没有找到') != -1:
                                    print('页面有，但是没有内容')
                                    break
                                cur_page = int(doc('.page .cur').text())
                                print('cur_page: ', cur_page,shop_catagory)
                                get_Shop_Info(driver,shop_catagory,happen_except,cur_page,shoplist_or_eachShop,city,each_url[0])
                                print('current area,shop catagory,max_page,cur_page: ', each_url[0], shop_catagory,max_page,cur_page)
                                for each_info in doc('.page .PageLink'):
                                    if int(pq(each_info).attr.title) > update_max_page:
                                        update_max_page = int(pq(each_info).attr.title)
                                if  update_max_page != max_page:
                                    print('max_page change,it maybe network wrong: ', max_page,update_max_page)
                                    max_page = update_max_page
                                print('max_page: ', max_page)
                                #write_to_db = True
                        else:
                            print('it only have one page ', each_url[0], shop_catagory, each_url[2])

                        if url_get_error == True:
                            break
                        print(len(all_shops))
                        cycle_counter = cycle_counter + 1
                        print('--------------------------- cycle_counter :',cycle_counter,shoplist_or_eachShop)
                        write_to_db = True
                        preserved_shop_list.append(shop_catagory)
                        insert_page = cur_page
                        happen_except = False
                        break
                    except:
                        #if latest_except_page <= cur_page and latest_except_page != 0 and len(all_shops) != 0:
                        #    write_to_db = True
                        #    print('except the same page for twice: ',cur_page,shop_catagory,each_url[1])
                        #    break
                        end_time = datetime.now()
                        print('start time,end time: ', start_time, end_time, (end_time - start_time).seconds)
                        print('except html content: ',driver.page_source)
                        print('except the same page for twice: ', cur_page, each_url[0],shop_catagory, each_url[2])
                        shop_num = len(all_shops)
                        record_info = 'except the same page for twice: ' + str(max_page) + '  '+ str(cur_page) + '  ' + each_url[0]+'  ' +shop_catagory + '  '+ str(shop_num) + '  ' + each_url[2] + '  '+ "\n"
                        with open(file_except,'a+', encoding="utf-8") as f:
                            f.write(record_info)
                        except_fail_num = except_fail_num + 1
                        if except_fail_num == 3:
                            url_get_error = True
                            break
                        print('except_fail_num: ',except_fail_num,each_url[0],shop_catagory)
                        #driver.close()
                        time.sleep(random.randint(20,35))
                        if cur_page > insert_page:
                            insert_page = cur_page
                        driver = get_brower_driver()
                        happen_except = True
                if happen_except == True:
                    print('it happen except,it dont write db')
                    break
                if url_get_error == True:
                    print('url_get_error happen ，and stop scrap')
                    break
                if write_to_db == True and len(all_shops) > 0:
                    db = pymysql.connect(host="127.0.0.1", user="root", passwd='axw19851111', db="can_yin_shop", charset="utf8")
                    cursor = db.cursor()
                    for each_info in all_shops:
                        try:
                            recomment_food = ''
                            for x in each_info.recommend_foodlist:
                                if x != '':
                                    recomment_food = recomment_food + ',' + x
                            print('recomment_food: ',recomment_food)

                            sta = cursor.execute(
                                'insert into shop_info_huoguo (shop_id,shop_name,address_info,shop_mainRegionName,shop_url,shop_city,shop_district,distance_km,shop_catagory,shop_subcatagory,shop_star,taste_score,environment_score,service_score,avgPrice,recommend_foods) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
                                % (each_info.shop_id,each_info.shop_name, each_info.address_info, each_info.shop_mainRegionName,each_info.shop_url, each_info.shop_city,each_info.shop_district,each_info.distance_km,
                                   each_info.shop_catagory,each_info.shop_subcatagory,each_info.shop_star,each_info.taste_score,each_info.environment_score,each_info.service_score,each_info.avgPrice,recomment_food
                                   ))
                            if sta == 1:
                                print('insert into shop_info success', each_info.shop_name, each_info.address_info, each_info.shop_url)
                            else:
                                print('insert into shop_info fail', each_info.shop_name, each_info.address_info, each_info.shop_url)
                            db.commit()
                        except:
                            except_list.append(each_info)
                            print('insert into shop_info except', each_info.shop_name, each_info.address_info, each_info.shop_url,shop_catagory)
                            insert_except = 'insert into shop_info except ' + each_info.shop_name + '  '+each_info.address_info + '  '+each_info.shop_url + '  '+ shop_catagory + '  ' + each_info.shop_district + ' except page index: '+ str(each_info.cur_index)+ ' max page: ' + str(max_page)+'\n'
                            with open(file_except, 'a+', encoding="utf-8") as f:
                                f.write(insert_except)
                    success_info = 'insert finish: ' + ' ' + each_url[0] + ' ' + shop_catagory + ' max page: '+ str(max_page) + ' valid page: '+ str(insert_page) + "\n"
                    with open(file_except, 'a+', encoding="utf-8") as f:
                        f.write(success_info)
                    db.close()
                    with open(preserved_file, 'a+', encoding="utf-8") as f:
                        content = each_url[0] + ' ' + each_url[1] + ' ' + each_url[2] + '\n'
                        ongoing_scraped_list.append(content)
                        f.write(content)

                #driver.close()
                end_time = datetime.now()
                print('start time,end time: ',start_time,end_time,(end_time-start_time).seconds)
                time.sleep(random.randint(2, 5))
                #time.sleep(random.randint(1, 10))
            for each in except_list:
                print('except_list', each.shop_name, each.address_info, each.shop_url)