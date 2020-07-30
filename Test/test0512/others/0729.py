#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @File : test_urllib.py
    @Author: LiJiaoyang
    @Date : 2020/5/13
    @Desc : 
'''

from urllib import request
from bs4 import  BeautifulSoup

def download_v1(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.'
                      '3683.86 Safari/537.36'
    }

    req = request.urlopen(url)
    data = req.read()
    print(data)



if __name__ == '__main__':
    url = 'https://www.zhihu.com/search?type=content&q=%E5%94%90%E4%BA%BA%E8%A1%97%E6%8E%A2%E6%A1%88'
    download_v1(url)