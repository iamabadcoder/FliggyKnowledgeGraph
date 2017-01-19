# -*- coding:utf-8 -*-

import json
import linecache

if __name__ == '__main__':
	file_path = '/Users/caolei/Desktop/qyer_recommended_tours_1.txt'
	dest_list = []
	for ith in range(1, len(open(file_path, 'rU').readlines()) + 1):
		ith_line = linecache.getline(file_path, ith)
		data = json.loads(ith_line)
		dest_list.append(data['DESTINATION'])
	print len(set(dest_list))
