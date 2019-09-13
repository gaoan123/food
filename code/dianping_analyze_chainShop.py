from DB_Handle import get_AllShops_specified_food,get_Chain_shops_for_specified_food
from shop_info_Commercial_area_specify_catagory_max_page import get_brower_driver
import time
from decode_encrypted_stream import css_get_for_shopDetails,decode_for_input_encrypted_stream,css_decode,css_decode_shoplist,css_get_for_shopFoodMenuList
from pyquery import PyQuery as pq
#from excel_handle import  write_chain_shops_food_menu_to_excel,append_chain_shop_menulist_for_excel
from excel_handle import  append_chain_shop_menulist_for_excel
import os


#shop_info = ['左庭右院鲜牛肉火锅', '69948722', '漕河泾/田林', '上海市徐汇区漕宝路徐汇日月光B1层B座', 'http://www.dianping.com/shop/69948722', '上海市', '徐汇区', '火锅']
shop_info = ['左庭右院鲜牛肉火锅', '65495748', '宝山城区', '上海市牡丹江路1569号宝乐汇5层', 'http://www.dianping.com/shop/65495748', '上海市', '崇明区', '火锅']
def get_allMenus_for_chain_shop(driver,shop_info):
    driver.get(shop_info[4])
    #driver.refresh()
    time.sleep(20)
    page_content = driver.page_source
    doc = pq(page_content)
    print('.mod .mod-title : ', doc('.mod .mod-title').html())
    print('doc(shop-closed).html() : ',doc('.shop-closed').html())
    commend_food_exist = str(doc('.mod .mod-title').html()).find('推荐菜')
    if commend_food_exist == -1:
        print('it dont include commend food: ',shop_info[0],shop_info[3],shop_info[4])
        return []
    if str(doc('.shop-closed').html()) != 'None':
        print('shop info invalid: ',shop_info[0],shop_info[3],shop_info[4])
        except_file = 'food_menulist_except'
        if os.path.exists(except_file) != True:
            fp = open(except_file, 'w')
            fp.close()
        except_info = 'shop info invalid: '+ ' '+shop_info[0] + ' ' + shop_info[3] + ' '+shop_info[4] +'\n'
        with open(except_file, 'a+', encoding="utf-8") as f:
            f.write(except_info)
        return []
    more_button_exist = False
    for each in doc('.shop-tab-recommend .unfold.J-more'):
        more_button_exist = True
    print('more_button_exist: ',more_button_exist)
    try:
        driver.find_elements('css selector','.shop-tab-recommend .unfold.J-more')[1].click()
        time.sleep(0.5)
        doc = pq(page_content)
        print(doc('.more-recommend-food').attr('href'))
        driver.find_element_by_css_selector('.more-recommend-food').click()
    except:
        driver.find_element_by_css_selector('.more-recommend-food').click()

    time.sleep(2)
    page_content = driver.page_source
    doc = pq(page_content)
    menulist = []
    for each in doc('.list-desc .shop-food-item'):
        #print(each)
        #print(pq(each))
        recommend_food = pq(each)('.shop-food-img img').attr('alt')
        print('recommend_food: ',recommend_food)
        recommend_count = pq(each)('.recommend-count').text()
        if recommend_count != '':
            recommend_count = int(recommend_count.split('人推荐')[0])
        else:
            recommend_count = 0
        print('recommend_count: ', recommend_count)
        recommend_reson = pq(each)('.recommend-reson-item').text()
        print('recommend_reson: ', recommend_reson)
        food_money = pq(each)('.shop-food-money').text()
        if food_money != '':
            food_money = int(food_money.split('￥')[1])
        else:
            food_money = 0
        print('food_money: ', food_money)
        menulist.append([recommend_food, recommend_count, food_money, recommend_reson])
    next_button = doc('.shop-food-list-page .next').text()
    while next_button == '下一页':
        driver.find_element_by_css_selector('.shop-food-list-page .next').click()
        time.sleep(0.5)
        page_content = driver.page_source
        doc = pq(page_content)
        next_button = doc('.shop-food-list-page .next').text()
        cur_page = doc('.shop-food-list-page .cur').text()
        print('current page for recommend food: ',cur_page)
        for each in doc('.list-desc .shop-food-item'):
            # print(each)
            # print(pq(each))
            recommend_food = pq(each)('.shop-food-img img').attr('alt')
            #print('recommend_food: ', recommend_food)
            recommend_count = pq(each)('.recommend-count').text()
            if recommend_count != '':
                recommend_count = int(recommend_count.split('人推荐')[0])
            else:
                recommend_count = 0
            #print('recommend_count: ', recommend_count)
            recommend_reson = pq(each)('.recommend-reson-item').text()
            #print('recommend_reson: ', recommend_reson)
            food_money = pq(each)('.shop-food-money').text()
            if food_money != '':
                food_money = int(food_money.split('￥')[1])
            else:
                food_money = 0
            print('+++++++++++++++++++++: ',[recommend_food,recommend_count,food_money,recommend_reson])
            menulist.append([recommend_food,recommend_count,food_money,recommend_reson])
            #print('food_money: ', food_money)
    return menulist

if __name__ == '__main__':
    specified_food = '火锅'
    city = '上海市'

    chain_shop_dict = get_Chain_shops_for_specified_food(specified_food, city)

    analyze_chain_shop = '那都不是锅港式打边炉'
    driver = get_brower_driver()
    driver.get('http://www.dianping.com/shanghai/ch10/g110')
    time.sleep(1)
    counter_valid = 0
    counter_invalid = 0
    for shop_name in chain_shop_dict.keys():
        if shop_name == analyze_chain_shop:
            print('chain_shop_dict[shop_name]: ',shop_name,len(chain_shop_dict[shop_name]))
            for shop_info in chain_shop_dict[shop_name]:
                print('****************************: ', shop_info)
                menulist = get_allMenus_for_chain_shop(driver, shop_info)
                time.sleep(1)
                #write_chain_shops_food_menu_to_excel(shop_info,menulist)
                if len(menulist) > 0:
                    append_chain_shop_menulist_for_excel(shop_info,menulist)
                    counter_valid = counter_valid + 1
                else:
                    counter_invalid = counter_invalid + 1
                print('chain_shop_dict[shop_name] len counter_valid,counter_invalid: ',counter_valid,counter_invalid)