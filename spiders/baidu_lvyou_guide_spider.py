# -*- coding:utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_guide_items_url():
	try:
		index_guide_list_container_ele = driver.find_element(by=By.ID, value="J-index-guide-list-container")
		for guide_item in index_guide_list_container_ele.find_elements_by_tag_name('a'):
			guide_items_url.append(guide_item.get_attribute("href"))
	except Exception, e:
		print Exception, ":", e


def click_next_page():
	try:
		curr_page_url = driver.current_url
		next_page_ele = driver.find_element_by_class_name('tangram-pager-next')
		next_page_ele.click()
		time.sleep(5)
		if curr_page_url != driver.current_url:
			return True
	except Exception, e:
		print Exception, ":", e
	return False


def crawl_target_page(driver, target_page_url):
	driver.get(target_page_url)
	time.sleep(4)
	get_guide_items_url()
	if click_next_page():
		return driver.current_url
	else:
		return None


if __name__ == '__main__':
	guide_items_url = []  # 记录所有攻略的URL
	driver = webdriver.Chrome('./drivers/chromedriver_mac_64')
	target_page_url = 'https://lvyou.baidu.com/guide/'
	while target_page_url:
		target_page_url = crawl_target_page(driver, target_page_url)

	for url in guide_items_url:
		driver.get(url)
		time.sleep(3)
		dl_pdf_eles = driver.find_elements_by_class_name("dl-pdf")
		for dl_pdf_ele in dl_pdf_eles:
			dl_pdf_ele.click()
			time.sleep(3)
			break
