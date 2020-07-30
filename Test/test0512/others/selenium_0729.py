#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @File : selenium_test.py
    @Author: LiJiaoyang
    @Date : 2020/5/13
    @Desc : 
'''

from selenium import  webdriver

headers = {
        "Referer": "https://www.zhizhu.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
    }

# 当运行该命令时，会弹出一个空的浏览器窗口
# 可以到下面的地址下载chromedirver,其他浏览器也一样
# http://npm.taobao.org/mirrors/chromedriver/
driver = webdriver.Chrome(r"D:\\chromedriver.exe")
# 如果想在选定的浏览器中加载网页，可以调用get()方法：
driver.get('https://www.zhihu.com/signup?next=%2F')
driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[1]/div/form/div[2]/div/label/input').send_keys('15620625028')
driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[1]/div/form/div[3]/div/label/input').send_keys('28268778q')
driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[1]/div/form/button').click()
# driver.find_element_by_id('kw').send_keys('python')
# driver.find_element_by_id('su').click()

# driver.close()

import time
time.sleep(10)
Cookies = driver.get_cookies()
print(Cookies)
cookie_dict = {}
import pickle
pickle.dump(Cookies, open("zhihu.cookie", "wb"))

for cookie in Cookies:
    cookie_dict[cookie["name"]] = cookie["value"]

# return Request(url=self.start_urls[0], dont_filter=True,headers=self.headers, cookies=cookie_dict)]