# -*- coding: UTF-8 -*-

from configobj import ConfigObj
import MySQLdb
from processing import *

def start_db_connection():
	# get config information by reading file "config.ini" 
	config = ConfigObj("config.ini")
	db_section = config["db"]
	db_host = db_section["db_host"]
	db_user = db_section["db_user"]
	db_pass = db_section["db_pass"]
	db_schema = db_section["db_schema"]
	# start sql connection
	db = MySQLdb.connect(db_host, db_user, db_pass, db_schema)
	return db


# count the data in the database
def get_count_info_database():
	db = start_db_connection()
	cursor = db.cursor()
	# check if table 5_star_seller_car exist
	check_table_exist_sql = "SELECT table_name FROM information_schema.TABLES WHERE table_name ='5_star_seller_car'"
	check_table_exist = cursor.execute(check_table_exist_sql)
	if check_table_exist == 0:
		create_table_sql = '''CREATE TABLE mobile_car_db.5_star_seller_car(
								id int(8) not null primary key auto_increment,
								brand char(20), 
								name char(40), 
								price char(10), 
								prod_date char(10), 
								prod_year char(5), 
								kilometers char(10), 
								power char(15), 
								no_accident bool, 
								HU_date char(10), 
								door char(5), 
								petrol boolean, 
								manual boolean, 
								other char(150))
							'''
		cursor.execute(create_table_sql)
	count_sql = "SELECT COUNT(*) FROM 5_star_seller_car"
	cursor.execute(count_sql)
	count = cursor.fetchone()[0]
	cursor.close()
	db.close()
	#print(count)
	return count

def search_repeated_car(cursor, name):
	repeated_car = 0
	check_repeat_sql = "SELECT EXISTS(SELECT * FROM 5_star_seller_car WHERE name = '"+ name +"')"
	try:
		cursor.execute(check_repeat_sql)
	except Exception as e:
		print(check_repeat_sql)
		raise e

	repeated_car = cursor.fetchone()[0]
	return repeated_car

# id, brand, name, price, prod_date, prod_year, kilometers, power, no_accident, HU_date, door, petrol, manual, other
def insert_data(count_id, list_name, list_price, list_info_1, list_info_2, set_update):
	db = start_db_connection()
	cursor = db.cursor()
	value = []
	brand_list = get_brand_from_name(list_name)
	for x in range(len(list_name)):
		item_tmp = []	
		item_tmp = [int(count_id), brand_list[x], list_name[x], int(list_price[x])]

		# prod_date, kilometers, power, prod_year
		list_detail_info_1 = get_details_from_1_line(list_info_1[x])
		item_tmp = item_tmp + list_detail_info_1

		# no_accident, HU_date, doors, petrol, manual, other
		if list_info_2:	
			list_detail_info_2 = get_details_from_2_line(list_info_2[x])
			item_tmp = item_tmp + list_detail_info_2
		else:
			item_tmp = item_tmp + [0,"","",0,0,""]

		# if update, need to avoid repeated data
		if set_update:
			repeated_car = search_repeated_car(cursor, list_name[x])
		# add only not repeated car item
		if repeated_car == 0:
			value.append(item_tmp)
			count_id = count_id + 1

	cursor.executemany('insert into 5_star_seller_car values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', value)
	# how many data added in the database
	count_add = len(value)
	db.commit()
	cursor.close()
	db.close()

	return count_add

if __name__ == '__main__':
	db = start_db_connection()
	cursor = db.cursor()
	result = search_repeated_car()