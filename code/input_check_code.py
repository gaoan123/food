import os
import pickle
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

def getDianPingCookies(brower): # get login taobao cookies
    url = "http://www.dianping.com/"
    brower.get("http://www.dianping.com/")
    brower.find_element_by_css_selector('.opt-btn.login').click()
    time.sleep(35)
    while True:
        print("Please login in taobao.com!")
        #time.sleep(3)
        # if login in successfully, url  jump to www.taobao.com
        while brower.current_url == url:
            print('brower.current_url == url')
            tbCookies = brower.get_cookies()
            brower.quit()
            cookies = {}
            for item in tbCookies:
                print('item[name],item[value]: ',item['name'],item['value'])
                cookies[item['name']] = item['value']
            outputPath = open('taobaoCookies.pickle','wb')
            pickle.dump(cookies,outputPath)
            outputPath.close()
            #brower.close()
            return cookies

def readDianPingCookies():
    # if hava cookies file ,use it # if not , getTaobaoCookies()
    if os.path.exists('taobaoCookies.pickle'):
        readPath = open('taobaoCookies.pickle','rb')
        tbCookies = pickle.load(readPath)
    else:
        tbCookies = getDianPingCookies()
    return tbCookies

def get_brower_driver():
    options = webdriver.FirefoxOptions()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
    profile = FirefoxProfile()
    profile.set_preference("general.useragent.override", user_agent)

    #options.add_argument('-headless')
    driver  = webdriver.Firefox(profile,options=options)
    url_prefer = 'http://www.dianping.com/'
    tbCookies = readDianPingCookies()
    #tbCookies = readDianPingCookies_for_allComments()
    driver.get(url_prefer)
    #brower.find_element_by_css_selector('.opt-btn.login').click()

    driver.implicitly_wait(3)  # 进行页面跳转或弹窗时需要设置等待时间，该句必不可少，不然就会定位不到弹窗或者新的页面内的元素
    #brower.find_element_by_class_name('bottom-password-login').click()

    for cookie in tbCookies:
        print('cookie,tbCookies[cookie]: ',cookie,tbCookies[cookie])
        driver.add_cookie({ "domain":"www.dianping.com",
                            "name":cookie,
                            "value":tbCookies[cookie],
                            "path":'/',
                            "expires":None })
    driver.get(url_prefer)
    time.sleep(1)
    #print('---------------: ',driver.page_source)
    return driver


def getDianPingCookies_for_allComments(brower): # get login taobao cookies
    url = 'http://www.dianping.com/shop/112133141'
    brower.get(url)
    time.sleep(2)
    brower.find_element_by_css_selector('.comment-all a').click()
    time.sleep(30)

    while True:
        print("Please login in taobao.com!")
        #time.sleep(3)
        # if login in successfully, url  jump to www.taobao.com
        print('brower.current_url: ',brower.current_url)
        while brower.current_url == 'http://www.dianping.com/shop/112133141/review_all':
            print('brower.current_url == url')
            tbCookies = brower.get_cookies()
            brower.quit()
            cookies = {}
            for item in tbCookies:
                print('item[name],item[value]: ',item['name'],item['value'])
                cookies[item['name']] = item['value']
            outputPath = open('allComments.pickle','wb')
            pickle.dump(cookies,outputPath)
            outputPath.close()

            return cookies

def readDianPingCookies_for_allComments():
    # if hava cookies file ,use it # if not , getTaobaoCookies()
    if os.path.exists('allComments.pickle'):
        readPath = open('allComments.pickle','rb')
        tbCookies = pickle.load(readPath)
    else:
        tbCookies = getDianPingCookies_for_allComments()
    return tbCookies

if __name__ == '__main__':
    #brower = webdriver.Firefox()
    #wait = WebDriverWait(brower, 10)
    #getDianPingCookies(brower)

    driver = get_brower_driver()
    getDianPingCookies_for_allComments(driver)
    #shop_url_tmp = 'http://www.dianping.com/shop/112133141'
    #driver.get(shop_url_tmp)
    #time.sleep(2)
    #driver.find_element_by_css_selector('.comment-all a').click()
    #time.sleep(3)


    #tbCookies = readDianPingCookies_for_allComments()
    #brower = webdriver.Firefox()
    #brower.get("http://www.dianping.com/")
    ##brower.find_element_by_css_selector('.opt-btn.login').click()
    #
    #brower.implicitly_wait(3)  # 进行页面跳转或弹窗时需要设置等待时间，该句必不可少，不然就会定位不到弹窗或者新的页面内的元素
    ##brower.find_element_by_class_name('bottom-password-login').click()
    #


    #for cookie in tbCookies:
    #    print('cookie,tbCookies[cookie]: ',cookie,tbCookies[cookie])
    #    driver.add_cookie({ "domain":"www.dianping.com",
    #                        "name":cookie,
    #                        "value":tbCookies[cookie],
    #                        "path":'/',
    #                        "expires":None })
    #driver.get('http://www.dianping.com/shop/112133141/review_all')

    #time.sleep(15)

    #tbCookies = readDianPingCookies_for_allComments()
    #driver = get_brower_driver()
   #brower.find_element_by_css_selector('.opt-btn.login').click()
    #url = 'http://www.dianping.com/shop/112133141'
    #driver.get(url)
    #time.sleep(2)
    #driver.find_element_by_css_selector('.comment-all a').click()
    #time.sleep(3)
    #for cookie in tbCookies:
    #   print('cookie,tbCookies[cookie]: ',cookie,tbCookies[cookie])
    #   driver.add_cookie({ "domain":"www.dianping.com",
    #                       "name":cookie,
    #                       "value":tbCookies[cookie],
    #                       "path":'/',
    #                       "expires":None })
#
    #driver.implicitly_wait(3)  # 进行页面跳转或弹窗时需要设置等待时间，该句必不可少，不然就会定位不到弹窗或者新的页面内的元素
#
    #time.sleep(3)