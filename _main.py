# -*- coding: UTF-8 -*-
import time
import re
import MySQLdb
from setup import *
from spider import *
from dbSQL import *

if __name__ == '__main__':

	# check how many data in the database
	count_id = get_count_info_database()
	if count_id:
		print("there are already " + str(count_id) + " data in the database...")
		print("-----------------------------------------------------------------------------")
	# start storing data with next line
	count_id = count_id + 1

	# get basic config info from file "config.ini"
	# ----------------+----------------+
	# basic_config[0] | basic_config[1]
	# ----------------+----------------+
	#   homepage_url  |   set_update
	basic_config = get_basic_config()
	url = basic_config[0]
	set_update = basic_config[1]

	# open the homepage and get page_source
	driver = get_homepage(url)
	# select some options to get different results
	driver = set_configuration(driver)

	for page_num in range(1,50):

		result = get_car_name_price(driver)
		name_list = result[0]
		price_list = result[1]

		if len(name_list) == len(price_list):
			result = get_car_detail_info(driver,name_list,price_list)
			info_1 = result[0]
			info_2 = result[1]
			if len(name_list) == len(info_1) :
				count_add = insert_data(count_id, name_list, price_list, info_1, info_2, set_update)
				print(" page " + str(page_num) + " is success !!! " )
				print(str(count_add) + " data have been added in the database...")
				count_id = count_id + count_add
				driver = get_next_page(driver)
			else :
				print("num of name is " + str(len(name_list)) + ", num of info is " + str(len(info)))
				driver = get_next_page(driver)
		else:
			print("num of name is " + str(len(name_list)) + ", num of info is " + str(len(info)))
			print(name_list)
			print(price_list)
			get_next_page(driver)
