#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @File : request_test.py
    @Author: LiJiaoyang
    @Date : 2020/5/13
    @Desc : 
'''

import requests

response = requests.get('https://github.com/timeline.json')
print(response.content)
print(response.text)

r = requests.post('http://httpbin.org/post')
print(r.text)

r = requests.put("http://httpbin.org/put")
print(r.text)

r = requests.delete("http://httpbin.org/delete")
print(r.text)

r = requests.head("http://httpbin.org/get")
print(r.text)

r = requests.options("http://httpbin.org/get")
print(r.text)