# -*- coding:utf-8 -*-

import os

if __name__ == '__main__':
	pdf_dir_path = '/Users/caolei/Downloads/baidu/baidu_pdf'
	html_dir_path = '/Users/caolei/Downloads/baidu/baidu_html'

	html_file_name_list = []
	pdf_file_name_list = []

	html_file_list = os.listdir(html_dir_path)
	for afile in html_file_list:
		if 'html' not in afile:
			continue
		html_file_name_list.append(os.path.splitext(afile)[0])
	print len(html_file_name_list)

	pdf_file_list = os.listdir(pdf_dir_path)
	for afile in pdf_file_list:
		if 'pdf' not in afile:
			continue
		pdf_file_name_list.append(os.path.splitext(afile)[0])
	print len(pdf_file_name_list)

	for name in pdf_file_name_list:
		if name not in html_file_name_list:
			print name

