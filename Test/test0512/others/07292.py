#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @File : 07292.py
    @Author: LiJiaoyang
    @Date : 2020/7/29
    @Desc : 
'''
import requests
from bs4 import  BeautifulSoup

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.'
                      '3683.86 Safari/537.36'
}

url = 'https://www.zhihu.com/search?q=%E5%94%90%E4%BA%BA%E8%A1%97%E6%8E%A2%E6%A1%88&type=content'
response = requests.get(url, headers=header)
data = response.text
# print(data)
soup = BeautifulSoup(data, 'html.parser')
fixed_html = soup.prettify()
print(fixed_html)

