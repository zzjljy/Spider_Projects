#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @File : request_test.py
    @Author: LiJiaoyang
    @Date : 2020/5/13
    @Desc : 
'''

import requests

response = requests.get('https://www.zhihu.com')
print(response.content)
print(response.text)

