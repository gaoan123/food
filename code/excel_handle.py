import xlwt
import xlrd
import os
import time
from DB_Handle import get_Chain_shops_counters_for_specified_food_in_city,delete_repeated_shops
from dianping_check_dir import get_analyze_whole_dir,analyze_check_and_create_dir,get_analyze_whole_dir,chain_shop_check_and_create_dir
import xlwt
# import xlutils;
from xlutils.copy import copy
import datetime
from scrap_all_menus import check_preserve_and_combie_file

def append_chain_shop_menulist_for_excel_include_price(shop_info,food_menu_list):
    chain_shop_dir = chain_shop_check_and_create_dir()
    filename = shop_info[0] + '.xls'
    filename = chain_shop_dir + filename
    file_exist = False
    if os.path.exists(filename) == False:
        excel_exist = True
        wb = xlwt.Workbook()
        ws = wb.add_sheet('1')
        # 合并第0行的第0列到第3列。
        ws.write_merge(0, 1, 0, 0, '店名')
        ws.write_merge(0, 1, 1, 1, '地址')
        ws.write(2, 0, shop_info[0])
        ws.write(2, 1, shop_info[3])
        file_exist = False

        wb.save(filename)
    else:
        file_exist = True

    rbook = xlrd.open_workbook(filename)
    count = len(rbook.sheets())
    for sheet in rbook.sheets():
        sheetname = sheet.name
        sheet = rbook.sheet_by_name(sheetname)
        rows = sheet.nrows
        cols = sheet.ncols
        print(sheetname, rows, cols)
        # 读取所有cell的内容
        # for i in range(rows):
        #    for j in range(cols):
        #        cell = sheet.cell_value(i, j)
        #        print('--------------------: ',cell)
        #

        # 读第一列找到文件的末尾，添加新的消息
        newWb = copy(rbook)
        newWs = newWb.get_sheet(0)
        # newWs = newWb.get_sheet(0)

        food_name_index = 2
        if file_exist == False:
            for each_food in food_menu_list:
                newWs.write_merge(0, 0, food_name_index, food_name_index + 1, each_food[0])
                newWs.write(1, food_name_index, '推荐人数')
                newWs.write(1, food_name_index + 1, '价格')

                newWs.write(2, food_name_index, each_food[1])
                newWs.write(2, food_name_index + 1, each_food[2])
                food_name_index = food_name_index + 2
        else:
            #merged_cells = sheet.merged_cells
            #print(merged_cells)
            #for (rlow, rhigh, clow, chigh) in merged_cells:
            #    print(rlow, rhigh, clow, chigh)
            newWs.write(rows, 0, shop_info[0])
            newWs.write(rows, 1, shop_info[3])
            order_food_menu_list = []
            have_order_food_list = []
            for j in range(2,cols):
                if j %2 == 0:
                    cell = sheet.cell_value(0,j)
                    print('--------------------: ',cell)
                    have_order_food_list.append(cell)
            print('order_food_list len: ',len(have_order_food_list))
            for have_each_index in range(0,len(have_order_food_list)):
                for new_each in food_menu_list:
                    if new_each[0] == have_order_food_list[have_each_index]:
                        order_food_menu_list.append([new_each,have_each_index])#列表，新取的food里存在已有的表格里时，记录已有表格里food所在的位置

            for each_food_and_index in order_food_menu_list:
                food_info = each_food_and_index[0]
                target_index = each_food_and_index[1]
                newWs.write(rows, 2 + target_index*2, food_info[1])
                newWs.write(rows, 2 + target_index*2 + 1, food_info[2])



        font = xlwt.Font()
        font.blod = True

        newWb.save(filename)

def append_chain_shop_menulist_for_excel(shop_info,food_menu_list):
    chain_shop_dir = chain_shop_check_and_create_dir()
    filename = shop_info[0] + '.xls'
    filename = chain_shop_dir + filename
    file_exist = False
    if os.path.exists(filename) == False:
        excel_exist = True
        wb = xlwt.Workbook()
        ws = wb.add_sheet('1')
        # 合并第0行的第0列到第3列。
        ws.write_merge(0, 1, 0, 0, '店名')
        ws.write_merge(0, 1, 1, 1, '地址')
        ws.write(2, 0, shop_info[0])
        ws.write(2, 1, shop_info[3])
        file_exist = False

        wb.save(filename)
    else:
        file_exist = True

    rbook = xlrd.open_workbook(filename)
    count = len(rbook.sheets())
    for sheet in rbook.sheets():
        sheetname = sheet.name
        sheet = rbook.sheet_by_name(sheetname)
        rows = sheet.nrows
        cols = sheet.ncols
        print(sheetname, rows, cols)
        # 读取所有cell的内容
        # for i in range(rows):
        #    for j in range(cols):
        #        cell = sheet.cell_value(i, j)
        #        print('--------------------: ',cell)
        #

        # 读第一列找到文件的末尾，添加新的消息
        newWb = copy(rbook)
        newWs = newWb.get_sheet(0)
        # newWs = newWb.get_sheet(0)

        food_name_index = 2
        if file_exist == False:
            for each_food in food_menu_list:
                newWs.write(0,food_name_index,each_food[0])
                newWs.write(1, food_name_index, '推荐人数')

                newWs.write(2, food_name_index, each_food[1])
                food_name_index = food_name_index + 1
        else:
            #merged_cells = sheet.merged_cells
            #print(merged_cells)
            #for (rlow, rhigh, clow, chigh) in merged_cells:
            #    print(rlow, rhigh, clow, chigh)
            newWs.write(rows, 0, shop_info[0])
            newWs.write(rows, 1, shop_info[3])
            order_food_menu_list = []
            have_order_food_list = []
            add_food_list = []
            for j in range(2,cols):
                 cell = sheet.cell_value(0,j)
                 print('--------------------: ',cell,sheet.cell_value(2,j),type(sheet.cell_value(2,j)))
                 have_order_food_list.append(cell)
            print('order_food_list len: ',len(have_order_food_list))
            for have_each_index in range(0,len(have_order_food_list)):
                for new_each in food_menu_list:
                    if new_each[0] not in have_order_food_list:
                        add_food_list.append(new_each)
                    if new_each[0] == have_order_food_list[have_each_index]:
                        order_food_menu_list.append([new_each,have_each_index])#列表，新取的food里存在已有的表格里时，记录已有表格里food所在的位置

            for each_food_and_index in order_food_menu_list:
                food_info = each_food_and_index[0]
                target_index = each_food_and_index[1]
                newWs.write(rows, 2 + target_index, food_info[1])
                #newWs.write(rows, 2 + target_index*2 + 1, food_info[2])

            # 这个shop新增的菜单，其他shop 相应推荐数为0
            if len(add_food_list) > 0:
                cols_end_index = cols
                print('cols:    ',cols)
                for each_add in add_food_list:
                    print('have another new menus comparing with other chain shop，cols_end_index: ', each_add,cols_end_index)
                    newWs.write(0, cols_end_index, each_add[0])
                    newWs.write(1, cols_end_index, '推荐人数')

                    for each_index in range(2,rows+1):
                        if each_index < rows:
                            newWs.write(each_index, cols_end_index, 0)
                        else:
                            newWs.write(each_index, cols_end_index, each_add[1])
                    cols_end_index = cols_end_index + 1

        font = xlwt.Font()
        font.blod = True
        newWb.save(filename)

def statistics_shop_chains_for_each_week(specify_food,city):
    code_city = {'北京市':'beijing','上海市': 'shanghai', '南京市':'nanjing', '成都市':'chengdu', '重庆市':'chongqing','武汉':'wuhan' ,  '深圳市':'shenzhen', '无锡市':'wuxi','长沙市':'changsha','杭州市':'hangzhou'}
    city_code = code_city[city]
    same_flag = check_preserve_and_combie_file(city_code,specify_food)
    #same_flag = True
    if same_flag == False:
        print('it have not scrap all menus,dont add statistics excel: ',city,specify_food)
        return
    analyze_dir = analyze_check_and_create_dir(specify_food)
    print('analyze_dir : ',analyze_dir)
    filename = specify_food + '实时统计' + '.xls'
    filename = analyze_dir + filename
    if os.path.exists(filename) == False:
        excel_exist = True
        wb = xlwt.Workbook()
        ws = wb.add_sheet(city)
        ws.write(0, 0,'店名')
        file_exist = False

        wb.save(filename)
    else:
        file_exist = True

    rbook = xlrd.open_workbook(filename)
    count = len(rbook.sheets())
    target_sheet_exist = False
    for sheet in rbook.sheets():
        sheetname = sheet.name
        if sheetname == city:
            print('it exist sheet')
            target_sheet_exist = True
            break
    if target_sheet_exist == False:
        newWb = copy(rbook)
        ws = newWb.add_sheet(city)
        ws.write(0, 0, '店名')
        file_exist = False
        newWb.save(filename)
        rbook = xlrd.open_workbook(filename)
        count = len(rbook.sheets())

    sheet_index = 0

    for sheet in rbook.sheets():
        sheetname = sheet.name
        if sheetname == city:
            target_sheet_exist = True
            sheet = rbook.sheet_by_name(sheetname)
            rows = sheet.nrows
            cols = sheet.ncols
            have_writed_shop_name_list = []
            if cols > 1:
                current_date = time.strftime("%Y-%m-%d", time.localtime())
                latest_record_date = sheet.cell_value(0, cols-1)
                if current_date == latest_record_date:
                    print('one day can only scrap a time: ',city,specify_food,latest_record_date)
                    return
                for i in range(1,rows):
                    cell = sheet.cell_value(i, 0)
                    have_writed_shop_name_list.append(cell)
                    print('**********************************************: ',cell)
            print(sheetname, rows, cols)
            newWb = copy(rbook)
            newWs = newWb.get_sheet(sheet_index)
            col_time = time.strftime("%Y-%m-%d", time.localtime())
            newWs.write(0, cols, col_time)
            rows_index = 1
            new_shops_list = []
            chain_shop_name_list = []
            chains_shops_num_dict = get_Chain_shops_counters_for_specified_food_in_city(specify_food, city)
            if len(chains_shops_num_dict) == 0:
                print('chains_shops_num_dict is 0,it dont start to scrap: ',city,specify_food)
                return
            for each_shop_name in chains_shops_num_dict.keys():
                chain_shop_name_list.append(each_shop_name)
                if cols > 1:#说明已经写入
                    row_shop_index = 1
                    new_shop_flag = True #有新的店进来
                    for each_shop in have_writed_shop_name_list:
                        if each_shop_name == each_shop:
                            newWs.write(row_shop_index, cols, int(chains_shops_num_dict[each_shop_name]))
                            new_shop_flag = False
                            break
                        else:
                            row_shop_index = row_shop_index + 1
                    if new_shop_flag == True:
                        print('it have new shop,and need to append the sheet: ',each_shop_name,int(chains_shops_num_dict[each_shop_name]))
                        new_shops_list.append([each_shop_name,int(chains_shops_num_dict[each_shop_name])])

                    newWs.write(rows_index, cols, int(chains_shops_num_dict[each_shop_name]))
                else:
                    newWs.write(rows_index, 0, each_shop_name)
                    newWs.write(rows_index, cols, int(chains_shops_num_dict[each_shop_name]))
                rows_index = rows_index + 1

            new_row_index = rows
            for new_shop in new_shops_list:
                newWs.write(new_row_index, 0, new_shop[0])
                for i in range(1,cols): #新的店数前几次抓取的都为0
                    newWs.write(new_row_index, i, 0)
                newWs.write(new_row_index, cols, new_shop[1])
                new_row_index = new_row_index + 1

            #新抓取的店里有些在之前的抓取的里面不存在，即可能店已经下架了
            for old_shop in have_writed_shop_name_list:
                if old_shop not in chain_shop_name_list:
                    if cols > 1:
                        for i in range(1, rows):
                            cell = sheet.cell_value(i, 0)
                            if old_shop == cell:
                                newWs.write(i, cols, 0)


            font = xlwt.Font()
            font.blod = True
            newWb.save(filename)
            break
        sheet_index = sheet_index + 1
    #if target_sheet_exist == False:



    #if target_sheet_exist == False:
#从excel表格里获得连锁店以及数量
def get_chain_shops_from_excel(specify_food,city):
    analyze_dir = analyze_check_and_create_dir(specify_food)
    filename = specify_food + '实时统计.xls'
    filename = analyze_dir + filename
    if os.path.exists(filename) == True:
        rbook = xlrd.open_workbook(filename)
        count = len(rbook.sheets())
        for sheet in rbook.sheets():
            sheetname = sheet.name
            if sheetname == city:
                sheet = rbook.sheet_by_name(sheetname)
                rows = sheet.nrows
                cols = sheet.ncols
                print(sheetname, rows, cols)
                # 读取所有cell的内容
                for i in range(1,rows):
                    shop_name = sheet.cell_value(i, 0)
                    shop_num = int(sheet.cell_value(i, cols-1))
                    print('--------------------: ',shop_name,shop_num)

def write_statistics_shop_chainsInfo_to_excel_for_specify_food_and_city():
    food_list = ['小龙虾','火锅','烧烤','小吃快餐','创意菜','韩国料理']
    city_list = ['上海市', '北京市', '深圳市', '南京市', '无锡市', '武汉', '长沙市', '成都市','重庆市','杭州市']
    for specify_food in food_list:
        for city in city_list:
            print('current food and city: ', specify_food, city)
            delete_repeated_shops(specify_food, city)
            statistics_shop_chains_for_each_week(specify_food, city)

#获取指定城市里的指定品类里，在一段时间内specify_duaring以天为单位，增长较快的请specify_ranking_num名
def calculate_differ_day(date_early,date_late):
    if date_early == date_late:
        print('differ_day: ', 0)
        return 0
    date1=time.strptime(date_early,"%Y-%m-%d")
    date2=time.strptime(date_late,"%Y-%m-%d")

    date1=datetime.datetime(date1[0],date1[1],date1[2])
    date2=datetime.datetime(date2[0],date2[1],date2[2])
    #返回两个变量相差的值，就是相差天数
    differ_day = str(date2 - date1).split(' ')[0]
    print('differ_day: ',differ_day)
    return int(differ_day)

def get_fastest_growth_chain_shop_info(specify_catagory,specify_city,specify_ranking_num,specify_duaring):
    analyze_dir = analyze_check_and_create_dir(specify_catagory)
    print('analyze_dir : ', analyze_dir)
    filename = specify_catagory + '实时统计' + '.xls'
    filename = analyze_dir + filename
    rbook = xlrd.open_workbook(filename)
    count = len(rbook.sheets())
    chain_shop_dict = {} #{'海底捞'：[[2019-01-02,30],[2019-01-20,35],[2019-03-20,42]}
    for sheet in rbook.sheets():
        sheetname = sheet.name
        if sheetname == specify_city:
            target_sheet_exist = True
            sheet = rbook.sheet_by_name(sheetname)
            rows = sheet.nrows
            cols = sheet.ncols
            for row_index in range(1,rows):
                if cols > 0:
                    shop_name = sheet.cell_value(row_index, 0)
                    chain_shop_dict[shop_name] = []
                    for col_index in range(1,cols):
                        scrap_date = sheet.cell_value(0, col_index)
                        shop_num = int(sheet.cell_value(row_index, col_index))
                        chain_shop_dict[shop_name].append([scrap_date,shop_num])
            break

    for shop_name in chain_shop_dict.keys():
        print(shop_name,chain_shop_dict[shop_name])
        date_index = 0
        counter = 0
        target_index_1 = 0
        target_index_2 = 0
        for each_info in chain_shop_dict[shop_name]:
            target_index_2 = len(chain_shop_dict[shop_name]) - 1
            date_latest = chain_shop_dict[shop_name][len(chain_shop_dict[shop_name]) - 1][date_index]
            print('date_latest,each_info[date_index]: ',date_latest,each_info[date_index])
            differ_day = calculate_differ_day(each_info[date_index],date_latest)
            if differ_day <= specify_duaring:
                target_index_1 = counter
                break
            counter = counter + 1
        print('target_index_1,target_index_2: ', target_index_1, target_index_2,chain_shop_dict[shop_name][target_index_1][0])
        break

    growth_shop_dict = {}
    for shop_name in chain_shop_dict.keys():
        growth_shop_dict[shop_name] = chain_shop_dict[shop_name][target_index_2][1] - chain_shop_dict[shop_name][target_index_1][1]

    sort_list = sorted(growth_shop_dict.items(), key=lambda d: d[1], reverse=True) #[('唐朝羊蝎子', 25), ('四川香天下火锅', 14), ('珑猫小火锅', 14), ('藏书羊肉', 11)]
    target_growth_list = []
    for each_info in sort_list[0:specify_ranking_num]:
        print(list(each_info))
        target_growth_list.append(list(each_info))
    return  target_growth_list





if __name__ == '__main__':

    #delete_repeated_shops(specify_food, city)
    #statistics_shop_chains_for_each_week(specify_food, city)
    #get_Chain_shops_counters_for_specified_food_in_city(specify_food,city)
    #statistics_shop_chains_for_each_week(specify_food,city)
    #append_chain_shop_menulist_for_excel(shop_info, food_menu_list)
    #get_chain_shops_from_excel(specify_food,city)
    case = 2
    if case == 1:
        specify_food = '火锅'
        city = '上海市'
        delete_repeated_shops(specify_food, city)
        statistics_shop_chains_for_each_week(specify_food, city)

    if case == 2:
        food_list = ['面馆', '粉面馆','粥粉面']
        city_list = ['上海市', '北京市', '深圳市', '南京市', '无锡市', '武汉', '长沙市', '成都市', '重庆市', '杭州市']
        for specify_food in food_list:
            for city in city_list:
                print('current food and city: ', specify_food, city)
                delete_repeated_shops(specify_food, city)
                statistics_shop_chains_for_each_week(specify_food, city)
    #food_list = ['火锅','烧烤']

    #str_early = '2019-03-11'
    #str_late = '2019-03-11'
    #calculate_differ_day(str_early,str_late)
    #get_fastest_growth_chain_shop_info('火锅','上海市',5, 6)

