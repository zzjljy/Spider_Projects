#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @File : main.py
    @Author: LiJiaoyang
    @Date : 2020/5/25
    @Desc : 爬虫文件debug
'''

from scrapy.cmdline import execute
import os
import sys
if __name__ == '__main__':

    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(['scrapy','crawl','image'])
