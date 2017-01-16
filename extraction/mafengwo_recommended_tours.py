# -*- coding:utf-8 -*-

__author__ = 'hackx'

import os
import re
import sys
import json
import linecache

reload(sys)
sys.setdefaultencoding('utf8')


# 写文件
def write_to_file(file_name, dest_name, tour_name, tour_desc):
	file_object = open(file_name, 'a+')
	tour_record = {}
	tour_record['DESTINATION'] = dest_name
	tour_record['TOUR_NAME'] = tour_name
	tour_record['TOUR_DESC'] = tour_desc
	file_object.write("%s\n" % json.dumps(tour_record, ensure_ascii=False))
	file_object.flush()
	file_object.close()


def extract_by_day(tour_desc, route_feature, route_design, route_detail):
	all_day = {}
	pattern = re.compile(r'D\d+')

	re_res1 = re.compile(route_design).search(tour_desc)
	if re_res1:
		tour_feature = tour_desc[:re_res1.start()]
		print tour_feature.replace(route_feature, '')

	re_res2 = re.compile(route_detail).search(tour_desc)
	if re_res2:
		tour_design = tour_desc[re_res1.end():re_res2.start()]
		tour_detail = tour_desc[re_res2.end():]

		tour_design_list = pattern.findall(tour_design)
		tour_detail_list = pattern.findall(tour_detail)

		if len(tour_design_list) == len(tour_detail_list):
			if len(tour_design_list) > 1:
				tour_design_split = pattern.split(tour_design)
				tour_detail_split = pattern.split(tour_detail)
				tour_design_split.remove(tour_design_split[0])
				tour_detail_split.remove(tour_detail_split[0])
				for i in range(len(tour_design_list)):
					curr_day = tour_design_list[i]
					one_day = {}
					one_day['POI'] = tour_design_split[i].replace(':', '').replace('：', '').split('——')
					one_day['DESC'] = tour_detail_split[i].replace(':', '').replace('：', '')
					all_day[curr_day] = one_day
			else:
				curr_day = 'ALL'
				one_day = {}
				tour_design_split = pattern.split(tour_design)
				tour_detail_split = pattern.split(tour_detail)
				one_day['POI'] = tour_design_split[0].replace(':', '').replace('：', '').split('——')
				one_day['DESC'] = tour_detail_split[0].replace(':', '').replace('：', '')
				all_day[curr_day] = one_day
		else:
			all_day['POI'] = tour_design.split('——')
			all_day['DESC'] = tour_detail.replace(':', '').replace('：', '')
	return all_day


def extract_by_day2(tour_desc, route_feature, route_detail):
	all_day = {}
	pattern = re.compile(r'D\d+')

	re_res1 = re.compile(route_detail).search(tour_desc)
	if re_res1:
		tour_feature = tour_desc[:re_res1.start()]
		print tour_feature.replace(route_feature, '')

		tour_detail = tour_desc[re_res1.end():]

		tour_detail_list = pattern.findall(tour_detail)

		if len(tour_detail_list) > 1:
			tour_detail_split = pattern.split(tour_detail)
			tour_detail_split.remove(tour_detail_split[0])
			for i in range(len(tour_detail_list)):
				curr_day = tour_detail_list[i]
				one_day = {}
				one_day['DESC'] = tour_detail_split[i]
				all_day[curr_day] = one_day
		else:
			curr_day = 'ALL'
			one_day = {}
			tour_detail_split = pattern.split(tour_detail)
			one_day['DESC'] = tour_detail_split[0]
			all_day[curr_day] = one_day
	return all_day


def get_tour_name(file_path, line_num):
	pre_line = linecache.getline(file_path, line_num - 1)
	if len(pre_line.replace('#', '').strip()) <= 90 and '方案' not in pre_line and '旅行时间' not in pre_line:
		return pre_line.replace('#', '').strip()
	else:
		return None


def get_tour_design(file_path, line_num, total_line_count):
	pass


def get_tour_desc(file_path, line_num, total_line_count):
	pass


def get_tour_feature(file_path, line_num):
	feature_line = linecache.getline(file_path, line_num).strip()
	pound_sign_count = feature_line.count('#')
	if '线路设计' in feature_line and '线路详情' in feature_line:
		tour_feature = feature_line[0:feature_line.find('线路设计')]
		tour_design = feature_line[feature_line.find('线路设计'):feature_line.find('线路详情')]
		tour_detail = feature_line[feature_line.find('线路详情'):]
		return tour_feature.replace('#', '').strip(), tour_design, tour_detail
	elif '线路设计' in feature_line:
		tour_feature = feature_line[0:feature_line.find('线路设计')]
		tour_design = feature_line[feature_line.find('线路设计'):]
		tour_detail = None
		return tour_feature.replace('#', '').strip(), tour_design, tour_detail
	elif '线路详情' in feature_line:
		tour_feature = feature_line[0:feature_line.find('线路详情')]
		tour_design = None
		tour_detail = feature_line[feature_line.find('线路详情'):]
		return tour_feature.replace('#', '').strip(), tour_design, tour_detail
	else:
		for jth in range(line_num + 1, line_num + 40):
			jth_line = linecache.getline(file_path, jth)
			jth_line_formated = jth_line.replace('#', '').strip()
			if jth_line_formated.startswith('线路设计') or jth_line_formated.startswith('线路详情'):
				break
			elif jth_line.count('#') < pound_sign_count:
				break
			elif jth_line.count('#') >= pound_sign_count:
				feature_line = feature_line + jth_line_formated
		return feature_line.replace('#', '').strip(), None, None


def extract_part_a(dir_path, afile, line_num, total_line_count):
	file_path = os.path.join(dir_path, afile)
	tour_name = get_tour_name(file_path, line_num)
	if tour_name is None:
		return
	# print tour_name
	tour_feature, tour_design, tour_detail = get_tour_feature(file_path, line_num)
	print tour_feature


# for ith in range(1, line_count + 1):
# 	ith_line = linecache.getline(file_path, ith)
# 	if '线路特色' in ith_line and '线路设计' in ith_line and '线路详情' in ith_line:
# 		tour_name = linecache.getline(file_path, ith - 1)
# 		pound_sign = ith_line[0:15].count('#')
# 		for jth in range(ith + 1, ith + 20):
# 			jth_line = linecache.getline(file_path, jth)
# 			if jth_line[0:15].count('#') == pound_sign:
# 				ith_line = ith_line.strip() + jth_line.replace('#', '').strip()
# 			else:
# 				break
#
# 		destination_name = os.path.splitext(afile)[0].replace('.html', '').replace(' ', '')
# 		tour_name = tour_name.replace('#', '').strip()
# 		tour_desc = ith_line.replace('#', '').strip()
# 		route_count += 1
#
# 		all_day = extract_by_day(tour_desc, '线路特色', '线路设计', '线路详情')
# 		write_to_file('mafengwo_recommended_tours.txt', destination_name, tour_name, all_day)
# print route_count


def keyword_unification(file_path):
	a = open(file_path, 'r')
	replaced_str = a.read().replace('线路安排', '线路设计').replace('线路指导', '线路设计')\
		.replace('线路行程', '线路详情').replace('简易行程','线路设计').replace('详细行程','线路详情')\
		.replace('具体行程', '线路详情')
	b = open(file_path, 'w')
	b.write(replaced_str)
	b.close()


if __name__ == '__main__':
	dir_path = '/Users/caolei/Downloads/mafengwo/mafengwo_md/todo'
	file_list = os.listdir(dir_path)
	for filtered_file in [afile for afile in file_list if 'html.md' in afile]:
		file_path = os.path.join(dir_path, filtered_file)
		keyword_unification(file_path)
		total_line_count = len(open(file_path, 'rU').readlines())
		for ith in range(1, total_line_count + 1):
			ith_line = linecache.getline(file_path, ith)
			if ith_line and ith_line.replace('#', '').strip().startswith('线路特色'):
				extract_part_a(dir_path, filtered_file, ith, total_line_count)
			else:
				pass
