# -*- coding:utf-8 -*-

import re
import os
import json
import linecache

if __name__ == '__main__':
	dir_path = './extraction/recommended_tours'
	all_destination = []
	all_lines = 0
	for filtered_file in [afile for afile in os.listdir(dir_path) if 'txt' in afile]:
		file_path = os.path.join(dir_path, filtered_file)
		data_source = filtered_file.split('_')[0]
		tour_destination = []
		tour_lines = 0
		for ith in range(1, len(open(file_path, 'rU').readlines()) + 1):
			ith_line = linecache.getline(file_path, ith)
			data = json.loads(ith_line)
			tour_destination.append(data['DESTINATION'])
			tour_lines += 1
			all_destination.append(data['DESTINATION'])
			all_lines += 1
		print '%s 涉及 %d 个目的地(去重), %d 条推荐线路' % (data_source, len(set(tour_destination)), tour_lines)
		for destination in set(tour_destination):
			print destination
	print '总: %d 个目的地(去重), %d 条推荐线路' % (len(set(all_destination)), all_lines)
	for destination in set(all_destination):
		print destination