import sys
import os

specify_food = '烧烤'
city = '深圳市'

#filename = 'analyze_result'
#if os.path.exists(filename) == True:


def get_trace_whole_dir():
    trace_dir = 'D:\\task_timer_exam\指定距离指定品类\can_yin\\url_generate\\'
    return trace_dir

def get_analyze_whole_dir():
    analyze_dir = 'D:\\task_timer_exam\指定距离指定品类\can_yin\\analyze_result\\'
    return analyze_dir

def chain_shop_check_and_create_dir():
    analyze_dir = get_analyze_whole_dir()
    chain_shop_dir = analyze_dir + 'chain_shops'
    if os.path.isdir(chain_shop_dir) == False:
        print('it not exist,creat: ',chain_shop_dir)
        os.makedirs(chain_shop_dir)
    else:
        print('it exist: ',chain_shop_dir)
    return chain_shop_dir + '\\'



def analyze_check_and_create_dir(specify_food):
    analyze_dir = get_analyze_whole_dir()
    analyze_food_dir = analyze_dir + specify_food
    if os.path.isdir(analyze_food_dir) == False:
        print('it not exist,creat: ',analyze_food_dir)
        os.makedirs(analyze_food_dir)
    else:
        print('it exist: ',analyze_food_dir)
    return analyze_food_dir + '\\'


def check_and_create_dir(city,specify_food):
    trace_dir = get_trace_whole_dir()
    food_dir = trace_dir + specify_food
    if os.path.isdir(food_dir) == False:
        print('it not exist,creat: ',food_dir)
        os.makedirs(food_dir)
    else:
        print('it exist: ',food_dir)

    food_city_dir = food_dir + '\\' + city
    if os.path.isdir(food_city_dir) == False:
        print('it not exist,creat: ',food_city_dir)
        os.makedirs(food_city_dir)
    else:
        print('it exist: ', food_city_dir)
    return food_city_dir + '\\'


if __name__ == '__main__':
    check_and_create_dir(city,specify_food)
