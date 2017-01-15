# -*- coding:utf-8 -*-

__author__ = 'hackx'

import os


# 目的地名称解析
def extract_destination(dir_path):
	destination_name_list = []
	file_list = os.listdir(dir_path)
	for file in file_list:
		if 'html.md' in file:
			file_name = os.path.splitext(file)[0]
			destination_name = file_name.replace(".html", '').replace('穷游锦囊 - ', '').replace('穷游锦囊-', '')
			print destination_name
			destination_name_list.append(destination_name)

	file_object = open('qyer_destinations.txt', 'a+')
	for line in destination_name_list:
		file_object.write("%s\n" % line)
		file_object.flush()
	file_object.close()


if __name__ == '__main__':
	dir_path = '/Users/caolei/Downloads/qyer/qyer_md/backup'
	extract_destination(dir_path)
