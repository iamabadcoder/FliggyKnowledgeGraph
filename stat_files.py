# -*- coding:utf-8 -*-

import re
import json
import linecache

if __name__ == '__main__':
	desc = '由于拜子龙湾较为偏远，所以行程一般分为两日游和三日游。两日游行程大致如下第一天从河内出发，前往码头登船，欣赏拜子龙湾的喀斯特地貌岩柱和湾畔景观；之后抵达云顿岛（Van DonIsland），欣赏岛屿风光，晚上住在渔民家中。第二天吃过早餐之后，骑自行车游览云顿岛北部地区，中午前后回到船上，继续欣赏拜子龙湾的美景。最后，于晚上回到河内'

	desc_2 = u'爱丁堡。第1天参加爱丁堡哈利·波特之旅（Harry PotterTrail），第2天听一听书和电影中都没有告诉你的故事'

	# desc_list = re.compile(ur'第[一|二]天').split(desc)

	desc_list = re.compile(ur'第\d+天').split(desc_2)

	print len(desc_list)

	for l in desc_list:
		print l

# file_path = '/Users/caolei/Desktop/qyer_recommended_tours_1.txt'
# dest_list = []
# for ith in range(1, len(open(file_path, 'rU').readlines()) + 1):
# 	ith_line = linecache.getline(file_path, ith)
# 	data = json.loads(ith_line)
# 	dest_list.append(data['DESTINATION'])
# print len(set(dest_list))
