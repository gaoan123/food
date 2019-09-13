from DB_Handle import get_specified_shop
from input_check_code import readDianPingCookies,readDianPingCookies_for_allComments
from decode_encrypted_stream import css_get_for_shopDetails,decode_for_input_encrypted_stream,css_decode,css_decode_shoplist
from pyquery import PyQuery as pq
import time
import jieba
from input_check_code import readDianPingCookies
from shop_info_Commercial_area_specify_catagory_max_page import get_brower_driver
from dianping_check_dir import get_analyze_whole_dir

from matplotlib import pyplot as plt

from wordcloud import WordCloud

from PIL import Image
import random
import numpy as np
import sys
import os

def get_pinglun_text_from_file():
    analyze_dir = get_analyze_whole_dir()
    filename = analyze_dir + 'pinglun.txt'
    pinglun_all_list = []
    with open(filename,encoding="utf-8") as f:
        for line in f.readlines():
            pinglun_all_list.append(line)
    print('pinglun len: ',len(pinglun_all_list))


def get_all_pinglun_for_specified_food(shop_info):
    analyze_dir = get_analyze_whole_dir()
    filename = analyze_dir + 'pinglun.txt'
    fp = open(filename, 'w')
    fp.close()
    shop_url = shop_info[4]
    driver = get_brower_driver()
    #shop_url_tmp = 'http://www.dianping.com/shop/112133141'
    driver.get(shop_url)
    time.sleep(10)
    driver.find_element_by_css_selector('.comment-all a').click()
    time.sleep(1)

    tbCookies = readDianPingCookies_for_allComments()
    for cookie in tbCookies:
        print('cookie,tbCookies[cookie]: ', cookie, tbCookies[cookie])
        driver.add_cookie({"domain": "www.dianping.com",
                           "name": cookie,
                           "value": tbCookies[cookie],
                           "path": '/',
                           "expires": None})

    shop_url_tmp = shop_url + '/review_all'
    driver.get(shop_url_tmp)
    time.sleep(1)
    page_content = driver.page_source
    doc = pq(page_content)

    dict_svg_text={}
    list_svg_y=[]
    dict_css_x_y={}
    pinglun_all_list = []
    love_Food_List = []
    dict_svg_text, list_svg_y, dict_css_x_y,shoplist_or_eachShop= css_get_for_shopDetails(doc)
    cur_page = doc('.reviews-pages .PageSel').text()
    max_page = 1
    print('cur_page: ',cur_page)
    for each in doc('.reviews-pages .PageLink'):
        max_page = pq(each).text()
        print(pq(each).text())

    while int(cur_page) <= int(max_page):

        pinglunLi = doc("div.reviews-items > ul > li").items()
        pinglun_index = 1
        for data in pinglunLi:
            #print(each)
            # 用户名
            print('cur_page,max_page,pinglun_index: ', cur_page, max_page,pinglun_index)
            userName = data("div.main-review > div.dper-info > a").text()
            # 用户ID链接
            if data("div.main-review > div.dper-info > a").text() != '匿名用户':
                userID = "http://www.dianping.com" + data("div.main-review > div.dper-info > a").attr("href")
            # 用户评分星级[10-50]
            startShop = str(data("div.review-rank > span").attr("class")).split(" ")[1].replace("sml-str", "")
            # 用户描述：机器：非常好 环境：非常好 服务：非常好 人均：0元
            describeShop = data("div.review-rank > span.score").text()
            print('describeShop: ', describeShop)
            # 关键部分，评论HTML,待处理，评论包含隐藏部分和直接展示部分，默认从隐藏部分获取数据，没有则取默认部分。（查看更多）
            pinglun = data("div.review-words.Hide").html()
            try:
                len(pinglun)
            except:
                pinglun = data("div.review-words").html()
            # 该用户喜欢的美食
            loveFood = data("div.main-review > div.review-recommend").text()
            # 发表评论的时间
            pinglunTime = data("div.main-review > div.misc-info.clearfix > span.time").text()
            print('old pinglun: ',pinglun)
            transfer_pinglun = css_decode_shoplist(dict_css_x_y, dict_svg_text, list_svg_y, pinglun)
            with open(filename, 'a+', encoding="utf-8") as f:
                f.write(transfer_pinglun + "\n")
            print("userName:", userName)
            print("userID:", userID)
            print("startShop:", startShop)
            print("describeShop:", describeShop)
            print("loveFood:", loveFood)
            print("pinglunTime:", pinglunTime)
            #print('before pinglun decode: ', pinglun)
            print("pinglun:", transfer_pinglun)
            pinglun_all_list.append(transfer_pinglun)
            print("*" * 100)
            pinglun_index = pinglun_index + 1
            if loveFood != '':
                love_Food_List.append(loveFood)

        if int(max_page) > 1 and int(cur_page) == int(max_page):
            break
        if int(cur_page) < int(max_page):
            driver.find_element_by_css_selector('.reviews-pages .NextPage').click()
            time.sleep(random.randint(3, 5))
            page_content = driver.page_source
            doc = pq(page_content)
            cur_page = doc('.reviews-pages .PageSel').text()
    print('pinglun_all_list: ',len(pinglun_all_list))

    return pinglun_all_list
#
#
##
def generate_wordCloud(pinglun_all_list):
    font = r'D:\task_timer_exam\指定距离指定品类\can_yin\code\ttf字体集合\MSYH.TTF'#设置字体
    #
    text = ''
    counter = 0
    for each in pinglun_all_list:
        print(each)
        print('-' * 100)
        counter = counter + 1
        print('counter:  ',counter + 1)
        text = text + each + '\n'
    #text = (open(r"C:\Users\ToOmMyY\Desktop\土味.txt")).read()
    #
    cut = jieba.cut(text)# 分词

    string =' '.join(cut)

    print(len(string))

    img = Image.open(r"D:\task_timer_exam\指定距离指定品类\can_yin\code\wordCloud.png")# 打开图片

    img_array = np.array(img)# 将图片装换为数组

    stopword = ['xa0']# 设置停止词，也就是你不想显示的词，这里这个词是我前期处理没处理好，你可以删掉他看看他的作用

    wc = WordCloud(

    background_color='white',#设置背景

    width=2000,#设宽

    height=1000,#设高

    mask=img_array,
    max_words=500,
    font_path=font,

    stopwords=stopword

    )

    wc.generate_from_text(string)# 绘制图片

    plt.imshow(wc)

    plt.axis('off')

    plt.figure()

    #plt.show()# 显示图片

    wc.to_file(r"D:\task_timer_exam\指定距离指定品类\can_yin\code\呼玛路xxx.png")# 保存图片

if __name__ == '__main__':
    shop_name = '那都不是锅'
    shop_addr = '呼玛路'
    shop_info = get_specified_shop(shop_name, shop_addr)
    print(shop_info)
    pinglun_all_list = get_all_pinglun_for_specified_food(shop_info)
    generate_wordCloud(pinglun_all_list)

    #font = r'D:\task_timer_exam\指定距离指定品类\can_yin\code\ttf字体集合\MSYH.TTF'  # 设置字体
    #text = '中了霸王餐，果然名不虚传，FM天天听到这家店广告，今天来体验下，先喝两碗汤，非常浓稠，再加汤就不好喝了，一定要先喝，海鲜和有机蔬菜都新鲜，非常干净，港式火锅第一次吃，感受不错'
    #cut = jieba.cut(text)
    #string = ' '.join(cut)
    #img = Image.open(r"D:\task_timer_exam\指定距离指定品类\can_yin\code\wordCloud.png")  # 打开图片
    #img_array = np.array(img)
    #stopword = ['xa0']  # 设置停止词，也就是你不想显示的词，这里这个词是我前期处理没处理好，你可以删掉他看看他的作用
    #wc = WordCloud(
    #    background_color='white',  # 设置背景
    #    width=2000,  # 设宽
    #    height=1000,  # 设高
    #    mask=img_array,
    #    font_path=font,
    #    stopwords=stopword
    #)
    #wc.generate_from_text(string)  # 绘制图片
    #plt.imshow(wc)
    #plt.axis('off')
    #plt.figure()
    ##plt.show()  # 显示图片
    #wc.to_file(r"D:\task_timer_exam\指定距离指定品类\can_yin\code\呼玛路xxx.png")  # 保存图片