import pymysql
#from excel_handle import write_chain_shops_to_excel
def get_specified_shop(shop_name,shop_addr):
    db = pymysql.connect(host="127.0.0.1", user="root", passwd='axw19851111', db="can_yin_shop", charset="utf8")
    cursor = db.cursor()
    #cursor.execute('''select * from shop_info where shop_name='那都不是锅港式打边*' ''')
    #cursor.execute('''select * from shop_info where shop_name REGEXP '^打边炉' ''')
    #cursor.execute('''select * from shop_info where shop_name like '%打边炉%' ''')
    cursor.execute('''select * from shop_info_huoguo where shop_catagory='火锅' ''')
    scrap_tuple = cursor.fetchall()
    target_list = []
    scrap_list = []
    for each_ele in scrap_tuple:
        scrap_tmp = list(each_ele)
        del scrap_tmp[0]
        #print(scrap_tmp)
        if scrap_tmp[0].find(shop_name) != -1 and scrap_tmp[3].find(shop_addr) != -1:
            target_list = list(scrap_tmp)
        scrap_list.append(scrap_tmp)

    print('total: ',len(scrap_list))
    print('taget len: ',len(target_list))

    return target_list

def get_AllShops_specified_food(specified_food,city):
    db = pymysql.connect(host="127.0.0.1", user="root", passwd='axw19851111', db="can_yin_shop", charset="utf8")
    cursor = db.cursor()
    #cursor.execute('''select * from shop_info where shop_name='那都不是锅港式打边*' ''')
    #cursor.execute('''select * from shop_info where shop_name REGEXP '^打边炉' ''')
    #cursor.execute('''select * from shop_info where shop_name like '%打边炉%' ''')
    cursor.execute('select * from shop_info_huoguo where (shop_catagory=%s and shop_city=%s)',(specified_food,city))
    scrap_tuple = cursor.fetchall()
    target_list = []
    scrap_list = []
    for each_ele in scrap_tuple:
        scrap_tmp = list(each_ele)
        del scrap_tmp[0]
        #print(scrap_tmp)
        if scrap_tmp[7].find(specified_food) != -1:
            target_list.append(list(scrap_tmp))
        scrap_list.append(scrap_tmp)

    print('total: ',len(scrap_list))
    print('taget len: ',city,specified_food,len(target_list))

    return target_list

def get_AllShops_specified_shop_and_city(specified_name,city):
    db = pymysql.connect(host="127.0.0.1", user="root", passwd='axw19851111', db="can_yin_shop", charset="utf8")
    cursor = db.cursor()
    #cursor.execute('''select * from shop_info where shop_name='那都不是锅港式打边*' ''')
    #cursor.execute('''select * from shop_info where shop_name REGEXP '^打边炉' ''')
    #cursor.execute('''select * from shop_info where shop_name like '%打边炉%' ''')
    cursor.execute('select * from shop_info_huoguo where (shop_name=%s and shop_city=%s)',(specified_name,city))
    scrap_tuple = cursor.fetchall()
    target_list = []
    scrap_list = []
    for each_ele in scrap_tuple:
        scrap_tmp = list(each_ele)
        del scrap_tmp[0]
        #print(scrap_tmp)
        target_list.append(list(scrap_tmp))
        scrap_list.append(scrap_tmp)

    print('total: ',len(scrap_list))
    print('taget len: ',city,len(target_list))

    return target_list


def get_AllShops_specified_food_old(specified_food):
    db = pymysql.connect(host="127.0.0.1", user="root", passwd='axw19851111', db="can_yin_shop", charset="utf8")
    cursor = db.cursor()
    #cursor.execute('''select * from shop_info where shop_name='那都不是锅港式打边*' ''')
    #cursor.execute('''select * from shop_info where shop_name REGEXP '^打边炉' ''')
    #cursor.execute('''select * from shop_info where shop_name like '%打边炉%' ''')
    cursor.execute('select * from shop_info_tmp where shop_catagory=%s',specified_food)
    scrap_tuple = cursor.fetchall()
    target_list = []
    scrap_list = []
    for each_ele in scrap_tuple:
        scrap_tmp = list(each_ele)
        del scrap_tmp[0]
        #print(scrap_tmp)
        if scrap_tmp[7].find(specified_food) != -1:
            target_list = list(scrap_tmp)
        scrap_list.append(scrap_tmp)

    print('total: ',len(scrap_list))
    print('taget len: ',len(target_list))

    return scrap_list




def get_Chain_shops_for_specified_food(specified_food,city):
    chain_dict = dict()
    chain_num = 0
    chain_no_num = 0
    sort_chain_shop = {}
    no_chain_shop = {}
    shop_name_index = 0
    shop_id_index = 1
    specified_food_list = get_AllShops_specified_food(specified_food,city)
    for each_ie in specified_food_list:
        if each_ie[shop_name_index] not in chain_dict:
            chain_dict[each_ie[shop_name_index]] = []
            chain_dict[each_ie[shop_name_index]].append(each_ie)
        else:
            chain_dict[each_ie[shop_name_index]].append(each_ie)
    print('len(chain_dict): ',len(chain_dict))
    while len(chain_dict) > 0:
        max_len = 1
        max_shop_name = ''
        for each_dict in chain_dict.keys():
            if len(chain_dict[each_dict]) > 1:
                if len(chain_dict[each_dict]) > max_len:
                    max_len = len(chain_dict[each_dict])
                    max_shop_name = each_dict
            else:
                no_chain_shop[each_dict] = chain_dict[each_dict]
                #chain_dict.pop(each_dict)
        if max_len > 1:
            sort_chain_shop[max_shop_name] = chain_dict[max_shop_name]
            chain_dict.pop(max_shop_name)
        else:
            for i in no_chain_shop.keys():
                chain_dict.pop(i)
    print('chain num,no chain num,sum: ',len(sort_chain_shop),len(no_chain_shop),len(sort_chain_shop)+len(no_chain_shop))
    for x in sort_chain_shop.keys():
        print(x,len(sort_chain_shop[x]))
        print('+' * 100)
    return sort_chain_shop

def get_Chain_shops_counters_for_specified_food_in_city(specified_food,city):
    chain_dict = dict()
    chain_num = 0
    chain_no_num = 0
    sort_chain_shop = {}
    no_chain_shop = {}
    shop_name_index = 0
    shop_id_index = 1
    specified_food_list = get_AllShops_specified_food(specified_food,city)
    for each_ie in specified_food_list:
        if each_ie[shop_name_index] not in chain_dict:
            chain_dict[each_ie[shop_name_index]] = []
            chain_dict[each_ie[shop_name_index]].append(each_ie)
        else:
            chain_dict[each_ie[shop_name_index]].append(each_ie)
    print('len(chain_dict): ',len(chain_dict))
    while len(chain_dict) > 0:
        max_len = 1
        max_shop_name = ''
        for each_dict in chain_dict.keys():
            if len(chain_dict[each_dict]) > 1:
                if len(chain_dict[each_dict]) > max_len:
                    max_len = len(chain_dict[each_dict])
                    max_shop_name = each_dict
            else:
                no_chain_shop[each_dict] = len(chain_dict[each_dict])
                #chain_dict.pop(each_dict)
        if max_len > 1:
            sort_chain_shop[max_shop_name] = max_len
            chain_dict.pop(max_shop_name)
        else:
            for i in no_chain_shop.keys():
                chain_dict.pop(i)
    print('chain num,no chain num,sum: ',len(sort_chain_shop),len(no_chain_shop),len(sort_chain_shop)+len(no_chain_shop))
    for x in sort_chain_shop.keys():
        print(x,sort_chain_shop[x])
        print('+' * 100)
    for each_name in no_chain_shop.keys():
        sort_chain_shop[each_name] = no_chain_shop[each_name]
    return sort_chain_shop

def delete_repeated_shops(specified_food,city):
    target_list = get_AllShops_specified_food(specified_food,city)
    no_repeat_list = []
    repeat_list = []
    shop_id_list = []
    for each_ie in target_list:
        if each_ie not in no_repeat_list:
            if each_ie[1] not in shop_id_list:
                shop_id_list.append(each_ie[1])
                no_repeat_list.append(each_ie)
            else:
                print('shop id same: ',each_ie)
            #no_repeat_list.append(each_ie)
        else:
            repeat_list.append(each_ie)
    print('total,no repeat,repeat: ', len(target_list), len(no_repeat_list), len(repeat_list),len(shop_id_list))
    db = pymysql.connect(host="127.0.0.1", user="root", passwd='axw19851111', db="can_yin_shop", charset="utf8")
    cursor = db.cursor()

    cursor.execute('delete from shop_info_huoguo where (shop_catagory=%s and shop_city=%s)', (specified_food, city))
    #cursor.execute('truncate table shop_info_huoguo')
#
    for each_info in no_repeat_list:
#
        sta = cursor.execute(
            'insert into shop_info_huoguo (shop_name,shop_id,shop_mainRegionName,address_info,shop_url,shop_city,shop_district,shop_catagory,shop_subcatagory,shop_star,taste_score,environment_score,service_score,avgPrice,recommend_foods,distance_km) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
            % (each_info[0], each_info[1], each_info[2], each_info[3], each_info[4], each_info[5], each_info[6],
               each_info[7], each_info[8], each_info[9], each_info[10], each_info[11], each_info[12], each_info[13],
               each_info[14], each_info[15]
               ))
        if sta != 1:
            print('insert into shop_info fail', each_info.shop_name, each_info.address_info, each_info.shop_url)
            # else:
#
    db.commit()
    db.close()



#from langconv import fanti_to_jianti

if __name__ == '__main__':
    shop_name = '那都不是锅'
    shop_addr = '呼玛路'
    shop_info = get_specified_shop(shop_name,shop_addr)
    #print(shop_info)
    #city = '武汉'
    #specified_food = '烧烤'
    #target_list = get_AllShops_specified_food(specified_food,city)

    code_city = ['北京市','上海市','南京市',  '成都市','重庆市', '武汉', '深圳市', '无锡市','长沙市', '杭州市']
    food_list = ['火锅','烧烤','江河湖海鲜','韩国料理','创意菜']
    for city in code_city:
        for specified_food in food_list:
            delete_repeated_shops(specified_food,city)

    ##print(len(target_list))
    #chain_shop_dict = get_Chain_shops_for_specified_food(specified_food,city)
    #print('chain_shop_dict: ',len(chain_shop_dict))
    #for each_info in chain_shop_dict:
    #    print(each_info)
#
    #write_chain_shops_to_excel(chain_shop_dict)