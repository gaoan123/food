import sys
import os

specify_food = '烧烤'
city = '深圳市'
trace_dir = 'D:\\task_timer_exam\指定距离指定品类\can_yin\\url_generate\\'
#filename = 'analyze_result'
#if os.path.exists(filename) == True:

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
