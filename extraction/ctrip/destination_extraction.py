# -*- coding:utf-8 -*-

import os


# 目的地名称解析
def extract_destination(dir_path):
	destination_name_list = []
	file_list = os.listdir(dir_path)
	for file in file_list:
		if 'html.md' in file:
			file_name = os.path.splitext(file)[0]
			destination_name = file_name.replace(".html", "").replace("旅游攻略", "")
			print destination_name
			destination_name_list.append(destination_name)

	with open('destination_extraction.txt', 'at') as f:
		for destination in destination_name_list:
			f.write("%s\n" % destination)


if __name__ == '__main__':
	dir_path = '/Users/caolei/Downloads/ctrip/ctrip_md/'
	extract_destination(dir_path)
