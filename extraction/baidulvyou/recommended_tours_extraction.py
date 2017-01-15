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
	file_object.write("%s >>>> %s >>>> %s\n" % (dest_name, tour_name, tour_desc))
	file_object.flush()
	file_object.close()


def find_next_ruote(file_path, i_line_num):
	i_line = linecache.getline(file_path, i_line_num)
	pound_sign_num = i_line.count('#')
	for j_line_num in range(int(i_line_num) + 1, int(i_line_num) + 100):
		j_line = linecache.getline(file_path, j_line_num)
		if j_line.count('#') == pound_sign_num:
			return j_line_num
		elif j_line.count('#') < pound_sign_num:
			break
	return -1


def extract_recommended_tours(dir_path, file_name):
	route_name_line_num_list = []  # 线路名称所在行号
	file_path = os.path.join(dir_path, file_name)
	file_lines_num = len(open(file_path, 'rU').readlines())
	for i_line_num in range(1, file_lines_num):
		i_line = linecache.getline(file_path, i_line_num)
		if i_line and '# 线路推荐' == i_line.strip():
			i_next_line = linecache.getline(file_path, i_line_num + 1)
			if i_next_line and '## SCHEDULE' == i_next_line.strip():
				i_next_next_line = linecache.getline(file_path, i_line_num + 2)
				if len(i_next_next_line.replace('#', '').strip()) <= 50:
					# print i_next_next_line.replace('#', '').strip()
					route_name_line_num_list.append(i_line_num + 2)
					next_ruote_line_num = find_next_ruote(file_path, i_line_num + 2)
					while next_ruote_line_num != -1:
						route_name_line_num_list.append(next_ruote_line_num)
						# print linecache.getline(file_path, next_ruote_line_num).replace('#', '').strip()
						next_ruote_line_num = find_next_ruote(file_path, next_ruote_line_num)
					print file_name, route_name_line_num_list

	if len(route_name_line_num_list) > 0:
		for route_name_line_num in route_name_line_num_list:
			all_day = {}
			route_name_line = linecache.getline(file_path, route_name_line_num)
			pound_sign = route_name_line.count('#')
			for i_line_num in range(route_name_line_num + 1, route_name_line_num + 500):
				i_line = linecache.getline(file_path, i_line_num)
				if i_line and i_line.count('#') == pound_sign:
					break
				elif pattern.search(i_line.replace('#', '').strip()):
					m = pattern.search(i_line.replace('#', '').strip())
					curr_day = {}
					if len(i_line.replace('#', '').strip()) <= 5:
						curr_day['POI'] = linecache.getline(file_path, i_line_num + 1).replace('#', '').strip()
						curr_day['POI'] = re.split(r'[-\s]\s*', curr_day['POI'])
					else:
						print i_line, m.end()
						curr_day['POI'] = i_line.replace('#', '').strip()[m.end()]
						curr_day['POI'] = re.split(r'[-\s]\s*', curr_day['POI'])

					desc_line = linecache.getline(file_path, i_line_num + 2).strip()
					for jth in range(i_line_num + 3, i_line_num + 20):
						jth_line = linecache.getline(file_path, jth)
						if jth_line[0:15].count('#') >= desc_line.count('#'):
							desc_line = desc_line + jth_line.replace('#', '').strip()
						else:
							break
					curr_day['DESC'] = desc_line.replace('#', '').strip()
					all_day[m.group()] = curr_day

			dest_name = os.path.splitext(file_name)[0].replace('.html', '').replace('百度旅游-', '').strip()
			tour_name = route_name_line.replace('#', '').strip()
			if len(all_day) > 0:
				write_to_file('recommended_tours_baidu.txt', dest_name, tour_name,
							  json.dumps(all_day, ensure_ascii=False))


if __name__ == '__main__':
	pattern = re.compile(r'D\d+')
	dir_path = '/Users/caolei/Downloads/baidu/baidu_md/todo'
	file_list = os.listdir(dir_path)
	for filtered_file in [afile for afile in file_list if 'html.md' in afile]:
		extract_recommended_tours(dir_path, filtered_file)
