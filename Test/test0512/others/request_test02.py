#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @File : request_test.py
    @Author: LiJiaoyang
    @Date : 2020/5/13
    @Desc : 
'''

import requests

payload = {'key1': 'value1', 'key2': ['value2', 'value3']}
r = requests.get('http://httpbin.org/get', params=payload)
print(r.url)
print(r.text)
print(r.encoding)
r.encoding = 'ISO-8859-1'
print(r.encoding)

url = 'http://example.webscraping.com/places/static/images/flags/af.png'
r = requests.get(url)
from PIL import Image
from io import BytesIO

print(r.content)
i = Image.open(BytesIO(r.content))
print(i)

r = requests.get('https://github.com/timeline.json')
print(r.json())

import requests
proxies = {'http': 'http://localhost:8888', 'https':'http://localhost:8888'}
url = 'http://www.baidu.com'
requests.post(url, proxies=proxies, verify=False) #verify是否验证服务器的SSL证书
