#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @File : BeautifulSoupTest.py
    @Author: LiJiaoyang
    @Date : 2020/5/13
    @Desc : 
'''

# coding=utf-8
from bs4 import  BeautifulSoup

proxies = {'http': 'http://localhost:8888', 'https':'http://localhost:8888'}

broken_html ='<ul class=country> <li>Area</li> <li>Population</ul>'
soup = BeautifulSoup(broken_html,'html.parser')
fixed_html = soup.prettify()

print(fixed_html)

# BeautifulSoup 能够正确解析缺失的引号并闭合标签

# 现在可以使用 find()和 findall()方法来定位我们需要的元素了 。
ul = soup.find('ul', attrs={'class': 'country'})
print(ul)
print(ul.find('li').text)
print(ul.find_all('li'))
'/html/body/div/ul[2]/li[4]/ul[1]/li/a[1]'
# print ul
# print ul.find('li')  # 只返回第一个
# print ul.find_all('li')