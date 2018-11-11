# -*- coding: UTF-8 -*-
import re

# get a brand_list from the name_list
def get_brand_from_name(name_list):
	brand_list = []
	for name in name_list:
		brand = name.split(" ")
		brand_list.append(brand[0])
	return brand_list

# prod_date, kilometers, power, prod_year
def get_details_from_1_line(info):
	detail_info_1 = info.split(",")
	while len(detail_info_1) < 3:
		detail_info_1.append("")

	# deal with kilometers
	detail_info_1[1] = ''.join(re.findall('[\d]+', detail_info_1[1]))

	# match new produced car
	new_car = re.findall('<b>(.*?)</b>', detail_info_1[0])
	if new_car:
			detail_info_1[0] = new_car
			prod_year = ["","2018"]
	else :
		# retrieve pro_year from pro_date
		prod_year = detail_info_1[0].split("/")
		if len(prod_year)<2:
				prod_year.append("")

	detail_info_1.append(int(prod_year[1]))

	return detail_info_1

# no_accident, HU_date, doors, petrol, manual, other
def get_details_from_2_line(info):
	detail_info_2 = []

	no_accident = re.findall('<b>(.*?)</b>', info)
	if no_accident:
		detail_info_2.append(1)
		info = re.sub('<b>(.*?)</b>', "", info)
	else:
		detail_info_2.append(0)

	HU_date = re.findall(",HU(.*?),",info)
	if HU_date:
		detail_info_2.append(HU_date[0])
		info = re.sub(',HU(.*?),', "", info)
	else:
		detail_info_2.append("")

	door = info[-3:]
	detail_info_2.append(door)
	info = re.sub(door,"",info)

	if "Benzin" in info:
		detail_info_2.append(1)
		info = re.sub("Benzin","",info)
	else:
		detail_info_2.append(0)

	if "Schaltgetriebe" in info:
		detail_info_2.append(1)
		info = re.sub("Schaltgetriebe","",info)
	else:
		detail_info_2.append(0)

	info = info.replace(","," ")
	info = re.sub(" +"," ", info)
	detail_info_2.append(info)

	return detail_info_2


if __name__ == '__main__':
	name_list = ["Mercedes-Benz Vaneo Compact Van 1.7 CDI", "Seat Ibiza 1.4 Sport Edition *KLIMA*KD+HU+ZAHNR. NEU*"]
	brand_list = get_brand_from_name(name_list)
	print(brand_list)
