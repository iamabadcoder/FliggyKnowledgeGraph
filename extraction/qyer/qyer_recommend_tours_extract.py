# -*- coding:utf-8 -*-

__author__ = 'hackx'

import os
import re
import json
import linecache

import sys

reload(sys)
sys.setdefaultencoding('utf8')


# 读取文件的指定行
def read_target_line(filename, line_num):
	return linecache.getline(filename, line_num)


#  定位指定行
def locate_target_line(file_path, target_line):
	line_num = 0
	for line in open(file_path):
		line_num += 1
		if target_line == line.strip():
			return line_num
	return -1


# 获取线路名称所在行号
def get_tour_name_line_nums(file_path):
	tour_name_line_nums = []
	target_line_num = locate_target_line(file_path, '# ___op___推荐路线___ed___')
	if target_line_num == -1:
		return tour_name_line_nums
	for i in range(target_line_num + 1, 2000):
		target_line = read_target_line(file_path, i)
		if target_line is None:
			print 'error when get_tour_name_line_nums, %s, %s' % (file_path, i)
			continue
		if target_line.startswith('# '):
			break
		elif target_line.startswith('## ___op___'):
			print target_line
			tour_name_line_nums.append(i)
	return tour_name_line_nums


# 获取目的地名称
def get_destination_name(afile):
	file_name = os.path.splitext(afile)[0]
	return file_name.replace('.html', '').replace('穷游锦囊 - ', '')


# 一天行程描述的解析
def get_one_day_desc(file_path, line_num):
	one_day_desc = ''
	which_day_line = read_target_line(file_path, line_num)
	ponud_sign_num = which_day_line.count('#')
	for i in range(line_num + 1, 2000):
		i_line = read_target_line(file_path, i)
		if '图：' in i_line:
			continue
		elif i_line.count('#') > ponud_sign_num:
			one_day_desc = one_day_desc + i_line.replace('#', '').strip()
		elif i_line.count('#') <= ponud_sign_num:
			break
	return one_day_desc.decode('utf8')


# 一条线路信息的解析
def extract_line_info(file_path, line_num, destination_name):
	all_day = {}
	tour_name_line = read_target_line(file_path, line_num).strip()
	if tour_name_line.startswith('## ___op___') and tour_name_line.endswith('___ed___'):
		print tour_name_line.replace('## ___op___', '').replace('___ed___', '').strip()
	else:
		print '线路名称有问题,' + tour_name_line
		return

	if '1日' in tour_name_line or '一日' in tour_name_line:  # 一日游线路解析
		tour_desc = ''
		for i in range(line_num + 1, 2000):
			i_line = read_target_line(file_path, i)
			if i_line.startswith('## ') or i_line.startswith('# '):
				break
			elif '图：' in i_line:
				continue
			else:
				tour_desc = tour_desc + i_line.replace('#', '').strip()
		one_day_dict = {}
		one_day_dict['DESC'] = tour_desc
		all_day['第1天'] = one_day_dict
	else:
		for i in range(line_num + 1, 2000):
			i_line = read_target_line(file_path, i)
			if i_line.startswith('## ') or i_line.startswith('# '):
				break
			elif re.search('第\d天', i_line) is not None and re.search('第\d天___ed___', i_line) is None:
				one_day = {}
				pattern = re.compile(r'第\d天：')
				result = pattern.search(i_line)
				if result:
					curr_day = result.group(0).replace('：', '')
					one_day['DESC'] = i_line.replace(result.group(0), '').replace('#', '').strip()
					all_day[curr_day] = one_day
			elif re.search('___op___第\d天___ed___', i_line) is not None:
				one_day = {}
				curr_day = i_line.replace('#', '').replace(prefix_sign, '').replace(postfix_sign, '').strip()
				one_day['DESC'] = get_one_day_desc(file_path, i)
				all_day[curr_day] = one_day
			else:
				print i_line
	# 写如文件
	file_object = open('qyer_tours.txt', 'a+')
	if len(all_day) >= 1:
		file_object.write("%s\t%s\t%s\n" % (
			destination_name, tour_name_line.replace('## ___op___', '').replace('___ed___', '').strip(),
			json.dumps(all_day, ensure_ascii=False)))
		file_object.flush()
	file_object.close()


# 解析推荐路线
def extract_tours(dir_path):
	file_list = os.listdir(dir_path)
	for afile in file_list:
		file_num = 1
		if 'html.md' in afile and file_num <= 200:
			file_num += 1
			file_path = os.path.join(dir_path, afile)
			destination_name = get_destination_name(afile)
			print destination_name
			tour_name_line_nums = get_tour_name_line_nums(file_path)
			print tour_name_line_nums
			for ln in tour_name_line_nums:  # ln 代表一条线路的开始
				extract_line_info(file_path, ln, destination_name)


if __name__ == '__main__':
	prefix_sign = '___op___'
	postfix_sign = '___ed___'
	dir_path = '/Users/caolei/Downloads/qyer/qyer_md/part_1'
	extract_tours(dir_path)
