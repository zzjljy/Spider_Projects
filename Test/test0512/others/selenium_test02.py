#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @File : selenium_test.py
    @Author: LiJiaoyang
    @Date : 2020/5/13
    @Desc : 
'''

from selenium import  webdriver

# 当运行该命令时，会弹出一个空的浏览器窗口
# 可以到下面的地址下载chromedirver,其他浏览器也一样
# http://npm.taobao.org/mirrors/chromedriver/
driver = webdriver.Chrome(r"D:\\chromedriver.exe")
# 如果想在选定的浏览器中加载网页，可以调用get()方法：
driver.get('https://www.baidu.com/')
driver.find_element_by_id('kw').send_keys('python')
driver.find_element_by_id('su').click()

# driver.close()