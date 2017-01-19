# -*- coding:utf-8 -*-

import os
import re
import sys
import json
import linecache

reload(sys)
sys.setdefaultencoding('utf8')


def write_to_file(file_name, dest_name, tour_name, tour_desc):
	file_object = open(file_name, 'a+')
	tour_record = {}
	tour_record['DESTINATION'] = dest_name
	tour_record['TOUR_NAME'] = tour_name
	tour_record['TOUR_DESC'] = tour_desc
	file_object.write("%s\n" % json.dumps(tour_record, ensure_ascii=False))
	file_object.flush()
	file_object.close()


def replace_sign(line):
	return line.replace(prefix_sign, '').replace(postfix_sign, '')


def extract_one_day_tours(file_path, ln, destination, pattern):
	all_day = {}
	one_day = {}
	tour_name_line = replace_sign(linecache.getline(file_path, ln)).replace('推荐路线｜', '').strip()

	if pattern.search(tour_name_line) is None:
		return
	pound_sign_count = tour_name_line.count('#')
	tour_desc = '  '
	for i in range(ln + 1, 2000):
		i_line = linecache.getline(file_path, i)
		if i_line.count('#') == pound_sign_count:
			break
		elif '图：' in i_line:
			continue
		else:
			tour_desc = tour_desc + i_line.replace('#', '').strip()
	poi_list = []
	pt = re.compile(r'___op___.*?___ed___')
	tour_poi = pt.findall(tour_desc)
	for poi in tour_poi:
		poi_list.extend(''.join(replace_sign(poi).split('-')).split('－'))  # 是错误的错误的错误的错误的错误的错误的错误的错误的
	one_day['POI'] = list(set(poi_list))
	one_day['DESC'] = replace_sign(tour_desc)

	all_day['第1天'] = one_day
	write_to_file('qyer_recommended_tours_2.txt', destination, tour_name_line.replace('#', ''), all_day)


def extract_two_day_tours(file_path, ln, destination, pattern):
	tour_name_line = replace_sign(linecache.getline(file_path, ln)).replace('推荐路线｜', '').strip()
	pound_sign_count = tour_name_line.count('#')
	if pattern.search(tour_name_line) is None:
		return
	tour_desc = ''
	for i in range(ln + 1, 2000):
		i_line = linecache.getline(file_path, i)
		if i_line.count('#') == pound_sign_count:
			break
		elif '图：' in i_line:
			continue
		else:
			tour_desc = tour_desc + i_line.replace('#', '').strip()

	all_day = {}

	pt_day_1 = re.compile(r'第\d+天')
	tour_desc_by_day = pt_day_1.split(tour_desc)

	if len(tour_desc_by_day) != 3:
		pt_day_2 = re.compile(r'第.*?天')
		tour_desc_by_day = []
		tour_desc_by_day = pt_day_2.split(tour_desc)

	if len(tour_desc_by_day) != 3:  # 未按天进行拆分，归结到一起，key使用ALL
		pt_poi = re.compile(r'___op___.*?___ed___')
		tour_poi = pt_poi.findall(tour_desc)
		poi_list = []
		for poi in tour_poi:
			poi_list.extend(replace_sign(poi).split('-'))
		one_day = {}
		one_day['POI'] = list(set(poi_list))
		one_day['DESC'] = replace_sign(tour_desc)
		all_day['ALL'] = one_day
	else:
		for i in range(1, len(tour_desc_by_day)):
			curr_day = {}
			curr_day_desc = tour_desc_by_day[i]
			curr_day_poi = []
			pt_poi = re.compile(r'___op___.*?___ed___')
			tour_poi = pt_poi.findall(curr_day_desc)
			for poi in tour_poi:
				curr_day_poi.extend(replace_sign(poi).split('-'))

			curr_day['POI'] = list(set(curr_day_poi))
			curr_day['DESC'] = replace_sign(curr_day_desc)
			all_day['第' + str(i) + '天'] = curr_day

	if len(all_day) > 0:
		write_to_file('qyer_recommended_tours_2.txt', destination, tour_name_line.replace('#', ''), all_day)


def extract_many_day_tours(file_path, ln, destination, pattern, which_day):
	tour_name_line = replace_sign(linecache.getline(file_path, ln)).replace('推荐路线｜', '').strip()
	pound_sign_count = tour_name_line.count('#')
	if pattern.search(tour_name_line) is None:
		return
	tour_desc = ''
	for i in range(ln + 1, 2000):
		i_line = linecache.getline(file_path, i)
		if i_line.count('#') == pound_sign_count:
			break
		elif '图：' in i_line:
			continue
		else:
			tour_desc = tour_desc + i_line.replace('#', '').strip()

	all_day = {}

	pt_day_1 = re.compile(r'第\d+天')
	tour_desc_by_day = pt_day_1.split(tour_desc)

	if len(tour_desc_by_day) != int(which_day) + 1:
		pt_day_2 = re.compile(r'第.*?天')
		tour_desc_by_day = []
		tour_desc_by_day = pt_day_2.split(tour_desc)

	if len(tour_desc_by_day) != int(which_day) + 1:  # 未按天进行拆分，归结到一起，key使用ALL
		pt_poi = re.compile(r'___op___.*?___ed___')
		tour_poi = pt_poi.findall(tour_desc)
		poi_list = []
		for poi in tour_poi:
			poi_list.extend(replace_sign(poi).split('-'))
		one_day = {}
		one_day['POI'] = list(set(poi_list))
		one_day['DESC'] = replace_sign(tour_desc)
		all_day['ALL'] = one_day
	else:
		for i in range(1, len(tour_desc_by_day)):
			curr_day = {}
			curr_day_desc = tour_desc_by_day[i]
			curr_day_poi = []
			pt_poi = re.compile(r'___op___.*?___ed___')
			tour_poi = pt_poi.findall(curr_day_desc)
			for poi in tour_poi:
				curr_day_poi.extend(replace_sign(poi).split('-'))

			curr_day['POI'] = list(set(curr_day_poi))
			curr_day['DESC'] = replace_sign(curr_day_desc)
			all_day['第' + str(i) + '天'] = curr_day

	if len(all_day) > 0:
		write_to_file('qyer_recommended_tours_2.txt', destination, tour_name_line.replace('#', ''), all_day)


def get_tour_name_line_nums(file_path):
	tour_name_line_nums = []
	line_count = len(open(file_path, 'rU').readlines())
	for ith in range(1, line_count + 1):
		ith_line = linecache.getline(file_path, ith)
		if ith_line is None:
			print 'error when get_tour_name_line_nums, %s, %s' % (file_path, ith)
			continue
		if ith_line.startswith('# ___op___推荐路线｜'):
			if len(ith_line) < 120:
				# print file_path, replace_sign(ith_line).replace('#', '').replace('推荐路线｜', '').strip()
				tour_name_line_nums.append(ith)
	return tour_name_line_nums


def extract_recommended_tours(file_name):
	destination = os.path.splitext(file_name)[0].replace('.html', '').replace('穷游锦囊 - ', '')

	file_path = os.path.join(todo_dir_path, file_name)

	pattern_list = [re.compile(r'[三|3]日'), re.compile(r'[四|4]日'), re.compile(r'[五|5]日'), re.compile(r'[六|6]日'),
					re.compile(r'[七|7]日'), re.compile(r'[八|8]日'), re.compile(r'[九|9]日')]

	# 一日游线路
	# pattern = re.compile(r'[一|1]日')
	# tour_name_line_nums = get_tour_name_line_nums(file_path)
	#
	# for ln in tour_name_line_nums:
	# 	extract_one_day_tours(file_path, ln, destination, pattern)


	# # 2日游线路
	# pattern = re.compile(r'[二|2|两]日')
	# tour_name_line_nums = get_tour_name_line_nums(file_path)
	#
	# for ln in tour_name_line_nums:
	# 	extract_two_day_tours(file_path, ln, destination, pattern)


	# 3日游线路
	pattern = re.compile(r'[九|9]日')
	tour_name_line_nums = get_tour_name_line_nums(file_path)

	for ln in tour_name_line_nums:
		extract_many_day_tours(file_path, ln, destination, pattern, 9)


def filter_specified_files():
	specified_files = {}
	for filtered_file in [afile for afile in file_list if 'html.md' in afile]:
		file_path = os.path.join(todo_dir_path, filtered_file)
		for ith in range(1, len(open(file_path, 'rU').readlines()) + 1):
			ith_line = linecache.getline(file_path, ith)
			if '# ___op___推荐路线｜' in ith_line.strip():
				# os.system("cp -f '" + file_path + "' " + part2_dir_path)  # 使用val接收返回值
				specified_files[filtered_file] = ith
				break
	return specified_files


if __name__ == '__main__':
	prefix_sign = '___op___'
	postfix_sign = '___ed___'
	todo_dir_path = '/Users/caolei/Downloads/qyer/qyer_md/todo'
	part2_dir_path = '/Users/caolei/Downloads/qyer/qyer_md/part2'
	file_list = os.listdir(todo_dir_path)
	filtered_files = filter_specified_files()
	for afile in sorted(filtered_files.keys()):
		extract_recommended_tours(afile)
