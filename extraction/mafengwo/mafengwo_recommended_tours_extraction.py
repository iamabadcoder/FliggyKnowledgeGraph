# -*- coding:utf-8 -*-

__author__ = 'hackx'

import os
import re
import sys
import json
import linecache

reload(sys)
sys.setdefaultencoding('utf8')


def keyword_unification(file_path):
	a = open(file_path, 'r')
	# replaced_str = a.read().replace('线路安排', '线路设计').replace('线路指导', '线路设计')\
	# 	.replace('线路行程', '线路详情').replace('简易行程', '线路设计').replace('详细行程', '线路详情')\
	# 	.replace('具体行程', '线路详情')
	replaced_str = a.read().replace('线路指导', '线路设计').replace('路线详情', '线路详情')
	b = open(file_path, 'w')
	b.write(replaced_str)
	b.close()


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


def extract_by_day(tour_desc, route_feature, route_design, route_detail):
	all_day = {}
	pattern = re.compile(r'D\d+')

	re_res1 = re.compile(route_design).search(tour_desc)
	if re_res1:
		tour_feature = tour_desc[:re_res1.start()]
		print tour_feature.replace(route_feature, '')

	re_res2 = re.compile(route_detail).search(tour_desc)
	if re_res2:
		tour_design = tour_desc[re_res1.end():re_res2.start()]
		tour_detail = tour_desc[re_res2.end():]

		tour_design_list = pattern.findall(tour_design)
		tour_detail_list = pattern.findall(tour_detail)

		if len(tour_design_list) == len(tour_detail_list):
			if len(tour_design_list) > 1:
				tour_design_split = pattern.split(tour_design)
				tour_detail_split = pattern.split(tour_detail)
				tour_design_split.remove(tour_design_split[0])
				tour_detail_split.remove(tour_detail_split[0])
				for i in range(len(tour_design_list)):
					curr_day = tour_design_list[i]
					one_day = {}
					one_day['POI'] = tour_design_split[i].replace(':', '').replace('：', '').split('——')
					one_day['DESC'] = tour_detail_split[i].replace(':', '').replace('：', '')
					all_day[curr_day] = one_day
			else:
				curr_day = 'ALL'
				one_day = {}
				tour_design_split = pattern.split(tour_design)
				tour_detail_split = pattern.split(tour_detail)
				one_day['POI'] = tour_design_split[0].replace(':', '').replace('：', '').split('——')
				one_day['DESC'] = tour_detail_split[0].replace(':', '').replace('：', '')
				all_day[curr_day] = one_day
		else:
			all_day['POI'] = tour_design.split('——')
			all_day['DESC'] = tour_detail.replace(':', '').replace('：', '')
	return all_day


def extract_by_day2(tour_desc, route_feature, route_detail):
	all_day = {}
	pattern = re.compile(r'D\d+')

	re_res1 = re.compile(route_detail).search(tour_desc)
	if re_res1:
		tour_feature = tour_desc[:re_res1.start()]
		print tour_feature.replace(route_feature, '')

		tour_detail = tour_desc[re_res1.end():]

		tour_detail_list = pattern.findall(tour_detail)

		if len(tour_detail_list) > 1:
			tour_detail_split = pattern.split(tour_detail)
			tour_detail_split.remove(tour_detail_split[0])
			for i in range(len(tour_detail_list)):
				curr_day = tour_detail_list[i]
				one_day = {}
				one_day['DESC'] = tour_detail_split[i]
				all_day[curr_day] = one_day
		else:
			curr_day = 'ALL'
			one_day = {}
			tour_detail_split = pattern.split(tour_detail)
			one_day['DESC'] = tour_detail_split[0]
			all_day[curr_day] = one_day
	return all_day


''' 一行同时包含线路特色、线路设计和线路详情三个关键词
### 西昌经典三日游线路
#### 线路特色：游览西昌最精华的景点，领略“月光城”的山水与城色。线路设计：D1：西昌——西昌卫星发射中心——西昌古城；D2：西昌——螺髻山；D3：泸山——邛海线路详情：D1：到达西昌后乘车前往素有“东方休斯敦”之称的——西昌卫星发射中心，可参观发射塔架、实体火箭、航天公园、奔月楼，了解神秘的中国航天高科技，能和发射架来一次合影一定是很骄傲的。下午回到西昌市区，乘公交到达西昌古城大通门，品尝地道西昌城门洞小吃，晚上游览西昌繁华夜市，登顶城楼赏“月光城”夜景。晚宿西昌市内。D2：上午乘车前往国家AAAA级风景名胜区——螺髻山。之后换乘景区观光车抵螺髻山索道站，乘亚洲落差最大的观光索道游览螺髻山美景，之后徒步进入螺髻山风景区，尽情享受原始森林天然氧吧，下山途中可车观螺髻山彝家山寨，这里有充满彝族特色的民居院落，彝族风情浓郁。晚上回到西昌市内住宿。D3：上午前往泸山风景区游览。泸山终年滴翠，山上有古柏、苍松、金桂，拥有多处道堂寺庙，佛道儒三教合一，世间罕见，还可参观中国唯一的彝族奴隶社会博物馆。之后乘车返回市区时，可顺便游览彝海结盟像，了解红军长征经过凉山的历史。下午可乘106巴士环湖一周，傍晚漫步邛海月色风情小镇、邛海公园，品尝特色醉虾和火盆烧烤，湖光山色，美酒佳肴，一醉方休。

## 三亚休闲四日游
### 线路特色：好景、好吃、好喝，驱除疲惫，激活身心的休闲之旅线路设计D1：大小洞天——南山寺——第一市场D2：三亚湾——椰梦长廊——鹿回头——大东海D3：西岛——天涯海角D4：亚龙湾——亚龙湾热带天堂森林公园线路详情D1：清晨朝拜道家文化胜地大小洞天，赏奇特秀丽的海景、山景和石景，还有历代诗文摩崖石刻，也需要凝神品味。中午可前往大小洞天旁的南山寺景区，品尝著名的“南山素斋”。下午在南山寺游玩，仰望高108米的壮观海上观音像。晚上不妨去三亚市区的第一市场来顿海鲜大餐，一天的疲惫准会一扫而光。D2：上午漫步椰梦长廊，穿梭碧绿如带的椰林，欣赏绚烂迷人的热带植物。午饭后可以前往拥有动人爱情传说的鹿回头山顶公园，强烈建议边走边看，一直在这里停留在傍晚时分，在鹿回头俯瞰三亚夜景相当美丽。晚上从鹿回头公园可以转战大东海一带，走走沙滩，吹吹海风，或者吃点海边露天烧烤，在酒吧喝到微醺，都是不错的选择。D3：上午出发前往西岛赏原始海岛风光，可参与潜水、海上摩托艇等各种海上运动。下午不妨到“天涯海角”寻找山盟海誓的爱恋，这里海水澄碧、椰林婆娑、奇石林立、水天一色，也是绝佳的海景观光地。D4：终于前往水清沙白的亚龙湾一睹三亚顶级海水浴场，沙滩游玩过后，可以前往附近的亚龙湾国家森林公园，坐着摆渡车翻山越岭，走过电影中的索桥，徜徉在清新的热带雨林中，为三亚之行画下圆满的句号。
'''


def extract_part_a(dir_path, afile):
	route_count = 0
	route_count = 0
	file_path = os.path.join(dir_path, afile)
	keyword_unification(file_path)
	line_count = len(open(file_path, 'rU').readlines())
	for ith in range(1, line_count + 1):
		ith_line = linecache.getline(file_path, ith)
		if '线路特色' in ith_line and '线路设计' in ith_line and '线路详情' in ith_line:
			tour_name = linecache.getline(file_path, ith - 1)
			pound_sign = ith_line[0:15].count('#')
			for jth in range(ith + 1, ith + 20):
				jth_line = linecache.getline(file_path, jth)
				if jth_line[0:15].count('#') == pound_sign:
					ith_line = ith_line.strip() + jth_line.replace('#', '').strip()
				else:
					break

			destination_name = os.path.splitext(afile)[0].replace('.html', '').replace(' ', '')
			tour_name = tour_name.replace('#', '').strip()
			tour_desc = ith_line.replace('#', '').strip()

			all_day = extract_by_day(tour_desc, '线路特色', '线路设计', '线路详情')
			if len(all_day) > 0:
				route_count += 1
				write_to_file('mafengwo_recommended_tours.txt', destination_name, tour_name, all_day)
	print route_count


''' 一行同时包含线路特色、线路安排和线路行程三个关键词
### 里斯本周边深度游
#### 线路特色：除了里斯本市内，市郊的世界遗产小镇辛特拉和邦德007的故乡卡斯凯什也一同包含在行程中，一次将里斯本地区的历史文化和自然风景都领略完成。（辛特拉和卡斯凯什介绍见17页）线路安排：D1 贝伦区(Belém)——希亚多(Chiado)——阿法玛地区(Alfama)——里斯本主教堂——圣若热城堡 (Castelo de São Jorge)(Sé Cathedral)——里斯本万国公园(Parque das Nacoes)D2 乘28路电车闲逛里斯本D3 辛特拉(Sintra)——佩纳宫(Palácio Nacional da Pena)——辛特拉王宫(Palácio Nacional de Sintra)——雷加莱拉庄园(Quinta da Regaleria)——罗卡角(Cabo da Roca)D4 卡斯凯什(Cascais)线路行程：D1 旅程从里斯本的风景集合处贝伦区(Belém)开始，在这里一路欣赏里斯本的几处地标性建筑，过后还可以在贝伦区最古老的蛋挞店品味一下最正宗的葡式蛋挞。接下来来到古老的希亚多(Chiado)地区，点一杯咖啡，坐在街边的餐厅感受里斯本浓浓的文化艺术气息。休息过后，步行前往里斯本最具特色的阿尔法玛区，在这里欣赏里斯本的最具异域风情的美丽街景。最后，来到万国公园体验一下现代的里斯本，伴着夕阳，一路游荡。D2 里斯本的28路电车是里斯本的一道独特风景线，它几乎经过里斯本所有的历史景点。第二天的旅行权当放松，跟着电车一路欣赏里斯本的街景也是不错的选择。傍晚，在Portas doSol观景台看完日落，步行前往里斯本最著名的法朵餐厅Clube do Fado，安静地听一曲温婉绝唱。D3从里斯本乘火车来到辛特拉，辛特拉是个小小的山城，这里风景十分秀丽，乘坐火车站出口处的434路公车可以参观辛特拉的绝大多数景点，包括佩纳宫(Palácio Nacional da Pena)和辛特拉王宫(Palácio Nacional de Sintra)等等，随上随下，很是方便。来辛特拉最不容错过的两个景点，当然要数雷加莱拉庄园(Quinta da Regaleria)和罗卡角(Cabo da Roca)。雷加莱拉庄园又称迷宫庄园，迷离的庄园奇景一定会让你为之沉醉。一天的游玩以罗卡角的落日结束，大西洋的落日绝对让你终生难忘！D4从罗卡角乘公交到卡斯凯什(Cascais)，这个小镇很是随意，如果愿意，可以来一次邦德之旅，游览曾经出现在《女王密使》中的帕拉西奥埃斯托利尔酒店(Palácio Estoril Hotel)和埃斯托里尔赌场。如果倦了，在小镇的海滨悠闲漫步也是不错的选择。
'''


def extract_part_b(dir_path, afile):
	route_count = 0
	file_path = os.path.join(dir_path, afile)
	# 统计文件行数
	line_count = len(open(file_path, 'rU').readlines())
	for ith in range(1, line_count + 1):
		ith_line = linecache.getline(file_path, ith)
		if '线路特色' in ith_line and '线路安排' in ith_line and '线路行程' in ith_line:
			tour_name = linecache.getline(file_path, ith - 1)
			pound_sign = ith_line[0:15].count('#')
			for jth in range(ith + 1, ith + 20):
				jth_line = linecache.getline(file_path, jth)
				if jth_line[0:15].count('#') == pound_sign:
					ith_line = ith_line.strip() + jth_line.replace('#', '').strip()
				else:
					break

			destination_name = os.path.splitext(afile)[0].replace('.html', '').replace(' ', '')
			tour_name = tour_name.replace('#', '').strip()
			tour_desc = ith_line.replace('#', '').strip()
			route_count += 1

			all_day = extract_by_day(tour_desc, '线路特色', '线路安排', '线路行程')
			if len(all_day) > 0:
				write_to_file('mafengwo_recommended_tours.txt', destination_name, tour_name, all_day)
	print route_count


'''
## 马岛 7日经典游
### 线路特色：来到马达加斯加最不可错过的当然是狐猴和猴面包树啦！线路设计：塔那那利佛——穆龙达瓦——昂达西贝——塔那那利佛
### 线路详情：D1：乘坐国际班机到达塔那那利佛之后，可以先在塔那停留一下，休息调整。（出行之前需要与旅行社接洽好接机时间等相关事项，这样出了机场就会有车和司机来接，方便开始之后的行程。）D2：在塔那，可以参观蓝山行宫、女王宫，再到独立大道逛逛。如果有买宝石或者木雕的打算可以到临街的商铺提前去询询价。D3：乘车去穆龙达瓦的猴面包树大道，车程需要4-5小时。D4：早上乘车横穿马达加斯加，到达东海岸的昂达西贝保护区，车程漫长，基本需要一天的时间。D5：昂达西贝雨林一日游D6：驱车前往塔那那利佛郊区的蝴蝶谷，再到达塔那市区。D7：购买纪念品，回国。

### 青岛主题四日游
##### 线路特色：一天一个主题，领略多面青岛。线路设计：D1：欧式建筑、老建筑群+黄金海岸沙滩一日游；D2：青岛海岸风光一日游；D3：青岛民俗文化一日游；D4：青岛山海风情一日游；
#### 线路详情：
##### D1：早餐过后，出门前备好泳衣。先到栈桥观赏回澜阁，游览第六海浴，接着按照老舍故居——迎宾馆——青岛基督教堂——观海上公园——总督府（现人大）——青岛路老建筑群——老舍公园——天主教堂的路线徒步游览。中午在中山路解决午餐，如春和楼、劈柴院特色小吃街、王姐烧烤等。下午，乘坐隧道3路到薛家岛交通枢纽，再转黄岛3路公交车到金沙滩，这是远东沙质最好的海滩，任你嬉戏玩耍。约18:00从金沙滩东站返回薛家岛，再转隧道2路回到青岛。D2：早餐过后，步行至海军博物馆，按照小青岛——鲁迅公园——青岛水族馆——青岛海底世界——小鱼山公园——汇泉湾第一海浴的路线前行游览，在汇泉广场美食节吃午餐。下午继续前往八大关，步行游览花石楼、元帅楼、公主楼、第二海浴，然后转到东海路雕塑街——音乐广场——五四广场——奥帆中心，观赏中国唯一水路两栖观光巴士“冒险鸭”、火炬、奥运五环、情人坝、奥帆白塔等，待夜幕降临时，静静地在海边欣赏夜景。晚上步行至云霄路美食街吃小吃，解决晚饭。D3：今天游览中山公园（植物园、榉林公园、首创电视塔、动物园、百花苑、西门出），游完后步行至老舍故居——青岛美术馆——海大鱼山校区，后从北门出前往龙山路地下商业街吃午饭。午饭过后，步行前往信号山公园，在公园山顶观赏岛城风貌后，下山步行至黄县路站，乘1、25、225路公交车至台东站下车，逛台东商业步行街——青岛文化街，再从天幕城北门进入，五彩穹顶非常适合拍照。游完后从南门出，来到登州路啤酒街，哈啤酒、吃蛤蜊、吃烧烤，酒足饭饱后还可回台东步行街逛逛夜市。D4：建议提前在酒店或网上预订崂山一日游团。因为崂山路途遥远，乘公交车费时费力，而且现在团体崂山游价格跟自助差不多。不想跟团，可以乘110路公交车到仰口景区，或乘104路公交车到太清宫景区。从崂山返程可以坐104路公交车。若想经济游的建议自带食物在山上解决午餐。从崂山下来后，可前往石老人海浴，这片沙滩干净而柔软，人也很少，适合游泳。回到市区后，若时间还够，可前往极地海洋世界，了解海洋生物的奇妙与自然。
'''


def extract_part_c(dir_path, afile):
	route_count = 0
	file_path = os.path.join(dir_path, afile)
	# 统计文件行数
	line_count = len(open(file_path, 'rU').readlines())
	for ith in range(1, line_count + 1):
		ith_line = linecache.getline(file_path, ith)
		ith_netx_line = linecache.getline(file_path, ith + 1)
		if '线路特色' in ith_line and '线路设计' in ith_line and ('线路详情' not in ith_line) and '线路详情' in ith_netx_line:
			tour_name = linecache.getline(file_path, ith - 1).strip()
			ith_netx_line_no_sharp = ith_netx_line.replace('#', '').strip()
			if len(ith_netx_line_no_sharp) >= 18:
				tour_name = linecache.getline(file_path, ith - 1)
				merge_line = ith_line.replace('#', '').strip() + ith_netx_line.replace('#', '').strip()
				# print tour_name + merge_line
				route_count += 1
			# dest_name = os.path.splitext(afile)[0].replace('.html', '').replace(' ', '')
			# write_to_file('mafengwo_tours.txt', dest_name, tour_name.replace('#', '').strip(), merge_line)
			else:
				merge_line = ith_line.replace('#', '').strip() + ith_netx_line_no_sharp.strip()
				pound_sign = ith_netx_line.count('#')
				for i in range(ith + 2, ith + 6):
					i_line = linecache.getline(file_path, i)
					if i_line.count('#') > pound_sign:
						merge_line = merge_line + i_line.replace('#', '').strip()
					else:
						break
					# print tour_name + merge_line
			route_count += 1
			dest_name = os.path.splitext(afile)[0].replace('.html', '').replace(' ', '')
			tour_name = tour_name.replace('#', '').strip()
			tour_desc = merge_line.replace('#', '').strip()

			all_day = extract_by_day(tour_desc, '线路特色', '线路设计', '线路详情')

			write_to_file('mafengwo_recommended_tours.txt', dest_name, tour_name, all_day)
	print route_count


'''
#### 赫尔辛基一日教堂文化之旅
###### 线路特色：来到赫尔辛基，风格各异、气势辉煌的几个主要教堂一定不容错过。因此一日之旅主要是在几大教堂间奔走体验，感受西方宗教文化与建筑风格。时间较紧，适合在赫尔辛基短暂停留的游客。
##### 线路设计
###### 上午：赫尔辛基中央火车站——议会广场——赫尔辛基大教堂——波罗的海的女儿雕像——乌斯别斯基东正教堂下午：阿黛浓国家美术馆——Kamppi购物广场——静默教堂——岩石教堂
##### 线路详情
###### 首先要游览的是赫尔辛基中央火车站，这是赫尔辛基最大的交通枢纽，四通八达。清晨的火车站人流量相对稀少，可以抓紧时间拍照（夏季天亮的很早，即使是7、8点钟，光线也是充足的）；在火车站乘坐2路电车经过3站到达Rautatieasema站，下车的地方正是议会广场。在议会广场的时候，你已经能远观赫尔辛基大教堂了。穿过广场，拾级而上，触摸教堂希腊式的廊柱，感受那一抹耀眼的白；接下来步行前往波罗的海的女儿雕像，细细欣赏那优雅的容颜。夏季时还可以靠近喷泉，伴着水花，丝丝凉意席卷而来。步行700米来到乌斯别斯基东正教堂，驻足观望墙壁上各式的壁画。下午吃完午饭后，乘坐4路电车回到赫尔辛基中央火车站，来到对面的阿黛浓国家美术馆。在这里找寻梵高的足迹以及拉斐尔的半身像。步行十分钟，来到kamppi购物广场一角的静默教堂。敲一敲这看起来像木桶饭的大教堂。进入教堂，关上门的瞬间，世界安静了。坐在木质的座椅上，做一个小小的祷告；最后，步行1公里前往岩石教堂，如果能赶上场音乐会演奏的话，可以体验一下教堂美妙的音效。静默教堂和阿黛浓国家美术馆位于商业购物广场附近，Forum，sokos，Kamppi都在附近，可根据时间安排购物。

### 体验冲绳魅力，欢乐购物 3日游
##### 线路特色：租车游览冲绳经典景点，行程轻松自在，购物在冲绳，深度发掘冲绳地区购物场所，尽情挑选浓郁日本风情产品。
#### 线路设计：
##### D1: 古宇利岛（古宇利大桥） — 海边咖啡馆 — 海族馆 — 万座毛（看夕阳）— 美国村 — 逛juscoD2: 首里城 — 小碌站—逛药妆店、百元店、AEON — 新都心（DFS、san-A main place)D3: 那霸空港（寄存行李、寄明信片） — 95番大巴奥特莱斯
#### 线路详情：
##### D1：由于要去的景点回城乘车不是很方便，所以可以选择包车出游，一般租车10小时35000日元。早餐后出发沿着冲绳最有名的的58国道向北行驶，沿着东海岸走。进入古宇利岛，首先要通过古宇利桥。这里海天相接，连成一线，风景异常美丽。午餐后前往冲绳必游的海族馆。同时万座毛看的美丽夕阳也是不能错过的绝佳美景，行程最终结束于西海岸的美国村上，傍晚返回市区。D2：为了有不一样的交通体验，我们选择了轻轨出行，建议购买一日通行劵。下车后可以选择步行方式前往首里城，沿路欣赏日本特样的风景。后乘轻轨前往小碌站，午餐后开始本次旅行的疯狂购物篇，药妆店、百元店、AEON 、DFS，都是猎物目标。D3：早起出发去波之上神宫，参拜宗神，10点前乘轻轨（昨天的一日票还能用）到空港寄存完行李，随后乘坐95番巴士前往奥特莱斯。乘坐时从空港国内线的三号门出去右手边的四号站台就是了。250日元/人，下车时投币。大约18分钟左右到达，后进行最后的购物血拼，为此次行程花上一个圆满的句号。
'''


def extract_part_d(dir_path, afile):
	route_count = 0
	file_path = os.path.join(dir_path, afile)
	# 统计文件行数
	keyword_unification(file_path)
	line_count = len(open(file_path, 'rU').readlines())
	for ith in range(1, line_count + 1):
		ith_line = linecache.getline(file_path, ith)
		if '线路特色' in ith_line:
			identify_line_a = linecache.getline(file_path, ith + 1).replace('#', '').strip().replace('：', '')
			identify_line_b = linecache.getline(file_path, ith + 3).replace('#', '').strip().replace('：', '')
			if identify_line_a and '线路设计' == identify_line_a and identify_line_b and '线路详情' == identify_line_b:
				route_design = identify_line_a + linecache.getline(file_path, ith + 2).replace('#', '').strip()
				route_detail = identify_line_b + linecache.getline(file_path, ith + 4).replace('#', '').strip()

				pound_sign = linecache.getline(file_path, ith + 4)[0:15].count('#')
				for jth in range(ith + 5, ith + 100):
					jth_line = linecache.getline(file_path, jth)
					if jth_line[0:15].count('#') == pound_sign:
						route_detail += jth_line.replace('#', '').strip()
					else:
						break

				tour_name = linecache.getline(file_path, ith - 1).replace('#', '').strip()
				tour_desc = (ith_line.strip() + route_design + route_detail).replace('#', '').strip()

				route_count += 1
				dest_name = os.path.splitext(afile)[0].replace('.html', '').replace(' ', '')
				all_day = extract_by_day(tour_desc, '线路特色', '线路设计', '线路详情')
				write_to_file('mafengwo_recommended_tours.txt', dest_name, tour_name, all_day)
	print route_count


'''
#### 首尔 4天“血拼”之旅
##### 线路特色：
###### 韩国是亚洲的又一个购物天堂，不少女孩来到韩国就是为了买东西，通过一个韩国之旅，准备出来一年的化妆品和服饰。
##### 线路设计：
###### 国内——首尔——国内
##### 线路详情：
###### D1：乘早班机从国内城市抵达首尔，到预订好的酒店办理好入住手续后，开始血拼之旅。第一站是首尔的购物天堂——明洞，这边的商业街时尚店铺林立，化妆品店一家挨着一家，并且基本上都配有中文导购，还有礼品送上。马路对面的乐天百货、Young Plaza也是相当好的购物去处，乐天免税店就在乐天百货内，可以买到免税的国际大牌。晚上还可以买票去看非常精彩搞笑的乱打秀，放松身心。D2：第二天转战梨大-新村-弘大一线，这里是韩国女生喜欢购物的地方，两所大学之间的路上聚集了许许多多的创意小店、精品店、咖啡厅，还有一些韩国潮牌的实体店，是女生们淘宝的好地方。弘大到了晚上更加的热闹，夜店酒吧分分开始营业，这里的一天才算真正开始。喜欢夜生活的朋友可以去感受一下韩国的夜店文化。D3：第三天可以到古色古香的三清洞和仁寺洞逛逛，这里浓浓的小清新气质会虏获不少少女心。这里较多的是装修精致，极富创意的咖啡馆和餐厅，还有一些服装饰品店，在这里可以放慢脚步，慢慢找寻你喜爱的宝贝。如果还是没有买到心中所想的那个它，晚上可以夜战东大门。东大门是韩国服饰最大的一个汇聚地，相信在这里你一定可以满意而归。D4：早上退房、寄存行李后，可以去到首尔著名的江南区，这里有“潮流前卫”的林荫路，也有“高档奢华”的清潭洞。看过《清潭洞爱丽丝》的蜂蜂对江南想必不会陌生，这里是首尔的富人区，代表着上流社会。江南区是首尔撞星几率最高的地区，著名的整形一条街也在江南区。逛完江南就回到酒店取行李，然后前往机场，结束此次旅行。

#### 首尔 4天“血拼”之旅
##### 线路特色
###### 韩国是亚洲的又一个购物天堂，不少女孩来到韩国就是为了买东西，通过一个韩国之旅，准备出来一年的化妆品和服饰。
##### 线路设计
###### 国内——首尔——国内
##### 线路详情
###### D1：乘早班机从国内城市抵达首尔，到预订好的酒店办理好入住手续后，开始血拼之旅。第一站是首尔的购物天堂——明洞，这边的商业街时尚店铺林立，化妆品店一家挨着一家，并且基本上都配有中文导购，还有礼品送上。马路对面的乐天百货、Young Plaza也是相当好的购物去处，乐天免税店就在乐天百货内，可以买到免税的国际大牌。晚上还可以买票去看非常精彩搞笑的乱打秀，放松身心。D2：第二天转战梨大-新村-弘大一线，这里是韩国女生喜欢购物的地方，两所大学之间的路上聚集了许许多多的创意小店、精品店、咖啡厅，还有一些韩国潮牌的实体店，是女生们淘宝的好地方。弘大到了晚上更加的热闹，夜店酒吧分分开始营业，这里的一天才算真正开始。喜欢夜生活的朋友可以去感受一下韩国的夜店文化。D3：第三天可以到古色古香的三清洞和仁寺洞逛逛，这里浓浓的小清新气质会虏获不少少女心。这里较多的是装修精致，极富创意的咖啡馆和餐厅，还有一些服装饰品店，在这里可以放慢脚步，慢慢找寻你喜爱的宝贝。如果还是没有买到心中所想的那个它，晚上可以夜战东大门。东大门是韩国服饰最大的一个汇聚地，相信在这里你一定可以满意而归。D4：早上退房、寄存行李后，可以去到首尔著名的江南区，这里有“潮流前卫”的林荫路，也有“高档奢华”的清潭洞。看过《清潭洞爱丽丝》的蜂蜂对江南想必不会陌生，这里是首尔的富人区，代表着上流社会。江南区是首尔撞星几率最高的地区，著名的整形一条街也在江南区。逛完江南就回到酒店取行李，然后前往机场，结束此次旅行。
'''


def extract_part_e(dir_path, afile):
	route_count = 0
	file_path = os.path.join(dir_path, afile)
	# 统计文件行数
	line_count = len(open(file_path, 'rU').readlines())
	for ith in range(1, line_count + 1):
		ith_line = linecache.getline(file_path, ith)
		if '线路特色' == ith_line.replace('#', '').replace('：', '').replace(':', '').strip():
			identify_line_a = linecache.getline(file_path, ith + 2).replace('#', '').strip().replace('：', '')
			identify_line_b = linecache.getline(file_path, ith + 4).replace('#', '').strip().replace('：', '')
			if identify_line_a and '线路设计' == identify_line_a and identify_line_b and '线路详情' == identify_line_b:
				route_feature = ith_line.replace('#', '').strip() + linecache.getline(file_path, ith + 1).replace('#',
																												  '').strip()
				route_design = identify_line_a + linecache.getline(file_path, ith + 3).replace('#', '').strip()
				route_detail = identify_line_b + linecache.getline(file_path, ith + 5).replace('#', '').strip()
				tour_name = linecache.getline(file_path, ith - 1).replace('#', '').strip()
				tour_desc = route_feature + route_design + route_detail
				route_count += 1

				dest_name = os.path.splitext(afile)[0].replace('.html', '').replace(' ', '')
				all_day = extract_by_day(tour_desc, '线路特色', '线路设计', '线路详情')
				write_to_file('mafengwo_recommended_tours.txt', dest_name, tour_name, all_day)
	print route_count


'''
## 吉隆坡休闲 3日游
#### 线路特色
### 景点、娱乐、购物，全面感受活力动感的吉隆坡。
#### 线路详情
### D1：上午参观国家清真寺和国家博物馆，之后前往苏丹亚都沙末大厦参观，搭乘轻铁Putra到双子塔，这是吉隆坡的标志。 D2：乘坐缆车前往云顶，感受丰富多彩的娱乐项目很多，去赌场小试运气。D3：前往小印度寻找风格奇特的装饰品，前往吉隆坡的购物场所体会购物乐趣，如果遇到购物嘉年华，超低的价格足以让游客疯狂。
'''


def extract_part_f(dir_path, afile):
	route_count = 0
	file_path = os.path.join(dir_path, afile)
	# 统计文件行数
	line_count = len(open(file_path, 'rU').readlines())
	for ith in range(1, line_count + 1):
		ith_line = linecache.getline(file_path, ith)
		if '线路特色' == ith_line.replace('#', '').replace('：', '').strip():
			identify_line_a = linecache.getline(file_path, ith + 2).replace('#', '').strip().replace('：', '')
			if identify_line_a and '线路详情' == identify_line_a:
				route_feature = ith_line.replace('#', '').strip() + linecache.getline(file_path, ith + 1).replace('#',
																												  '').strip()
				tour_name = linecache.getline(file_path, ith - 1).replace('#', '').strip()
				if '备选路线' in tour_name:
					continue
				route_detail = identify_line_a
				pound_sign = linecache.getline(file_path, ith + 2).count('#')
				first_line = True
				for i in range(ith + 3, ith + 6):
					i_line = linecache.getline(file_path, i)
					if i_line.count('#') > pound_sign:
						first_line = False
						route_detail = route_detail + i_line.replace('#', '').strip()
					else:
						if first_line:
							route_detail = route_detail + i_line.replace('#', '').strip()
						break
				tour_desc = route_feature + route_detail
				route_count += 1

				if '线路设计' in route_feature:
					continue

				dest_name = os.path.splitext(afile)[0].replace('.html', '').replace(' ', '')
				all_day = extract_by_day2(tour_desc, '线路特色', '线路详情')
				write_to_file('mafengwo_recommended_tours.txt', dest_name, tour_name, all_day)
	print route_count


if __name__ == '__main__':
	dir_path = '/Users/caolei/Downloads/mafengwo_old/mafengwo_md/todo'
	file_list = os.listdir(dir_path)
	for filtered_file in [afile for afile in file_list if 'html.md' in afile]:
		extract_part_a(dir_path, filtered_file)
		extract_part_b(dir_path, filtered_file)
		extract_part_c(dir_path, filtered_file)
		extract_part_d(dir_path, filtered_file)
		extract_part_e(dir_path, filtered_file)
		extract_part_f(dir_path, filtered_file)
