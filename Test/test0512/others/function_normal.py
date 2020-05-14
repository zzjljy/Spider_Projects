#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @File : function_normal.py
    @Author: LiJiaoyang
    @Date : 2020/5/13
    @Desc : 
'''

from urllib import parse
import os

#py2中用法：urlparse.urlparse
domain = parse.urlparse("https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/spiders.html")
print(domain)
dir, name = os.path.split(domain.path)
print(dir)
print(name)
