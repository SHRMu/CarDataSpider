# -*- coding: UTF-8 -*-
import re
import time

def get_car_name_price(driver):
	# name_list
	name_list = []
	re_name = '<span class="h3 u-text-break-word">(.*?)</span>'
	names = re.findall(re_name, driver.page_source)
	# clean name with '
	for name in names:
		name = name.replace("'"," ")
		name_list.append(name)
	# price_list
	price_list = []
	re_price = '<span class="h3 u-block">(.*?)</span>'
	prices = re.findall(re_price, driver.page_source)
	# filer useless characters, remain only price number
	for price in prices:
		price = ''.join(re.findall('[\d]+', price))
		price_list.append(price)
	return [name_list,price_list]
	

def get_car_detail_info(driver,name_list,price_list):
	info_line_1 = []
	info_line_2 = []
	re_info = '<div class="rbt-regMilPow">(.*?)</div></div>'
	info_list = re.findall(re_info, driver.page_source)
	for item in info_list:
		# first line info: year, kilometers, power
		re_1 = '(.*?)</div><div>'
		result = re.findall(re_1, item)
		info_line_1.append("".join(result[0].split()))
		# second line info: wait for optimization
		re_2 = '</div><div>(.*?)Türen</div>'
		result = re.findall(re_2, item)
		if result:
			info_line_2.append("".join(result[0].split()))
		else:
			info_line_2.append("")
	return [info_line_1,info_line_2]

def get_next_page(driver):
	time.sleep(60)
	elem_link = driver.find_element_by_class_name("next-resultitems-page")
	driver.get(elem_link.get_attribute("data-href"))
	return driver