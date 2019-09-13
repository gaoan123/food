from matplotlib import pyplot as plt
from DB_Handle import get_AllShops_specified_shop_and_city,get_Chain_shops_for_specified_food
#num_list = [1.5, 0.6, 7.8, 6]
#plt.bar(range(len(num_list)), num_list)
#plt.show()
from excel_handle import get_fastest_growth_chain_shop_info
from dianping_check_dir import get_analyze_whole_dir

#specified_food = '火锅'
#city = 'shanghai'

#chain_shop_num_list = []
#chain_shop_name_list = []
#target_list = get_AllShops_specified_food(specified_food)
#for i in target_list:
#    print(i)
#print(len(target_list))
#chain_shop_dict = get_Chain_shops_for_specified_food(target_list)
#print('chain_shop_dict: ',len(chain_shop_dict))
#for shop_name in chain_shop_dict.keys():
#    if len(chain_shop_dict[shop_name]) > 10:
#        chain_shop_name_list.append(shop_name)
#        chain_shop_num_list.append(len(chain_shop_dict[shop_name]))

def draw_statitics_chain_shops_pic(title,fastest_growth_list):
    chain_shop_name_list = []
    chain_shop_num_list = []
    for each_info in fastest_growth_list:
        chain_shop_name_list.append(each_info[0])
        chain_shop_num_list.append(each_info[1])

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.title(title)
    blist = plt.barh(range(len(chain_shop_num_list)), chain_shop_num_list, color='rgb', tick_label=chain_shop_name_list)
    for a, b in zip(chain_shop_num_list, range(0, len(chain_shop_name_list))):
        plt.text(a + 1, b, '%.0f' % a, ha='center', va='center', fontsize=7)
    for b in blist:
        print(b.get_height(), b.get_x())
    whole_dir = get_analyze_whole_dir() + 'generate\\' + 'shop_static.jpg'
    plt.savefig('test2.jpg')


if __name__ == '__main__':
    city = '成都市'
    specified_food = '火锅'
    date_duration = 6
    rank_num = 5
    fastest_growth_list = get_fastest_growth_chain_shop_info(specified_food,city,rank_num, date_duration)
    title = str(date_duration) + '天内' + city + specified_food + '前' + str(rank_num) + '名'
    draw_statitics_chain_shops_pic(title, fastest_growth_list)

    #获得每个店的信息
    for each_info in fastest_growth_list:
        shop_name = each_info[0]
        target_list = get_AllShops_specified_shop_and_city(shop_name,city)
        for each_shop in target_list:
            print(each_shop)
        print('*' * 100)
    #plt.show()
