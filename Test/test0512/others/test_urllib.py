#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @File : test_urllib.py
    @Author: LiJiaoyang
    @Date : 2020/5/13
    @Desc : 
'''

from urllib import request

def download_v1(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.'
                      '3683.86 Safari/537.36'
    }
    req = request.urlopen(url)
    data = req.read()
    print(data)


if __name__ == '__main__':
    url = 'http://zhidao.baidu.com/search?'
    download_v1(url)