# -*- coding:utf-8 -*-

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


# 读取文件的指定行
def read_target_line(filename, lineno):
	return linecache.getline(filename, lineno)


def locate_target_line(file_path, target_line):
	line_num = 0
	for line in open(file_path):
		line_num += 1
		if target_line == line.strip():
			return line_num
	return -1


def get_day_str(line):
	day_str = line.replace('#', '').lstrip(' ')
	res = re.search(ur"[a-zA-Z0-9]+", day_str.decode('utf8'))
	if res is not None:
		res_span = res.span()
		print res_span[0]
		return day_str[res_span[0]:res_span[1]]
	else:
		return 'D1'


# 一天行程poi的解析
def get_one_day_poi(file_path, line_num, poi):
	last_poi_line_num = line_num
	one_day_poi = ''
	tour_poi_line = read_target_line(file_path, line_num)
	pound_sign_num = tour_poi_line.count('#')
	if poi is not None:
		one_day_poi = poi
	for i in range(line_num + 1, 1000):
		i_line = read_target_line(file_path, i)
		if i_line.count('#') == pound_sign_num:
			one_day_poi = one_day_poi + i_line.replace('#', '').strip().strip('\n')
			last_poi_line_num = i
		else:
			break
	one_day_poi_utf8 = one_day_poi.strip().decode('utf8')

	one_day_poi_list = []
	if '→' in one_day_poi:
		one_day_poi_list = one_day_poi_utf8.split('→')
	elif '-' in one_day_poi and '→' not in one_day_poi:
		one_day_poi_list = one_day_poi_utf8.split('-')
	elif '—' in one_day_poi and '→' not in one_day_poi:
		one_day_poi_list = one_day_poi_utf8.split('—')
	elif '－' in one_day_poi and '→' not in one_day_poi:
		one_day_poi_list = one_day_poi_utf8.split('－')
	else:
		one_day_poi_list.append(one_day_poi_utf8)
	return one_day_poi_list, last_poi_line_num


# 一天行程描述的解析
def get_one_day_desc(file_path, line_num):
	one_day_desc = ''
	tour_poi_line = read_target_line(file_path, line_num)
	ponud_sign_num = tour_poi_line.count('#')
	for i in range(line_num + 1, 800):
		i_line = read_target_line(file_path, i)
		if 'TIPS' in i_line:
			break
		elif i_line.count('#') > ponud_sign_num:
			one_day_desc = one_day_desc + i_line.replace('#', '').strip()
		elif i_line.count('#') <= ponud_sign_num:
			break
	return one_day_desc.decode('utf8')


# 一条线路的解析过程
def get_tour_poi_and_desc(file_path, line_num, destination_name):
	all_day = {}
	tour_name_line = read_target_line(file_path, line_num)
	print tour_name_line
	for i in range(line_num + 1, 500):
		i_line = read_target_line(file_path, i)
		if i_line.startswith('## ') or i_line.startswith('# '):
			break
		elif re.search(special_sign, i_line) is not None:
			search_res = re.search(special_sign, i_line).span()
			one_day = {}
			curr_day = i_line[0:search_res[0]].replace('#', '').strip()
			if curr_day == '':
				if '一日' in tour_name_line:
					curr_day = 'D1'
				else:
					curr_day = 'ALL'
			one_day['POI'], last_poi_line_num = get_one_day_poi(file_path, i, i_line[search_res[1]:])
			one_day['DESC'] = get_one_day_desc(file_path, last_poi_line_num)
			all_day[curr_day] = one_day
		else:
			print i_line
	if len(all_day) > 0:
		write_to_file('ctrip_recommended_tours.txt', destination_name, tour_name_line.replace('#', '').strip(), all_day)


def get_tour_name_line_nums(file_path, target_line_num):
	tour_name_line_nums = []
	for i in range(target_line_num + 1, 500):
		target_line = read_target_line(file_path, i)
		if target_line is None:
			print 'error when get_tour_name_line_nums, %s, %s' % (file_path, i)
			continue
		if target_line.startswith('# '):
			break
		elif target_line.startswith('## ') and ('行程综述' not in target_line) and ('行程踪述' not in target_line):
			print target_line.strip()
			tour_name_line_nums.append(i)
	return tour_name_line_nums


# 解析行程推荐
def extract_recommended_tours(file_name):
	file_path = os.path.join(dir_path, file_name)
	destination = os.path.splitext(file_name)[0].replace('.html', '').replace('旅游攻略', '')
	target_line_num = locate_target_line(file_path, '# 行程推荐')
	if target_line_num != -1:
		tour_name_line_nums = get_tour_name_line_nums(file_path, target_line_num)
	else:
		return
	for ln in tour_name_line_nums:  # ln 代表一条线路的开始
		print get_tour_poi_and_desc(file_path, ln, destination)


if __name__ == '__main__':
	dir_path = '/Users/caolei/Downloads/ctrip/ctrip_md/todo'
	special_sign = read_target_line(dir_path + '/万象旅游攻略.html.md', 180)[7:10]
	file_list = os.listdir(dir_path)
	for filtered_file in [afile for afile in file_list if 'html.md' in afile]:
		extract_recommended_tours(filtered_file)
