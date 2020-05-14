#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @File : test01.py
    @Author: LiJiaoyang
    @Date : 2020/5/12
    @Desc : 
'''

import requests
import sqlite3
from bs4 import BeautifulSoup
from urllib import parse


dblocation = r'D:\zl_datas\data_database\Sqlite\Spider_teste.sqlite3'
coon = sqlite3.connect(dblocation)
cur = coon.cursor()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'
}
# 加上这句话fiddler可以抓到请求包
proxies = {'http': 'http://localhost:8888', 'https': 'http://localhost:8888'}


def get_one_page(url):
    response = requests.get(url, headers=headers, proxies=proxies)
    print(response.encoding)
    if response.status_code == 200:
        return response

def main():
    url = 'http://61.240.19.180:6080/arcgis/rest/services/JN/JNYX0826/MapServer'
    html = get_one_page(url)
    # print(html)
    soup = BeautifulSoup(html.text, 'lxml')
    # print(soup)
    # 格式haul输出
    # print(soup.prettify())
    # results = soup.select('.rbody>ul>li>ul>li')
    # print(results)
    i = 0
    for ul in soup.select('.rbody>ul>li>ul'):
        for item in ul.select('li>a'):
            print(item)
            # print(dir(item))
            print(item.get_text())
            a_text = item['href']
            url_item = parse.urljoin('http://61.240.19.180:6080', a_text)
            print(url_item)
            image = requests.get(url_item, headers=headers)
            # text返回的是unicode型的数据，一般是在网页的header中定义的编码形式
            # content返回的是bytes二进制型的数据
            pic_name = str(i)+'.jpg'
            print(pic_name)
            # with open(pic_name, 'wb') as f:
            img = image.content
            print(img)
            # cur.execute('INSERT INTO spider_0512(id,img_name,image) VALUES(?,?,?)',
            #             (i, str(i), sqlite3.Binary(img)))
                # f.write(image.content)
                # print(image.content)
            i += 1
            print('-------------------------------------------')
    cur.execute('select image from spider_0512 where id=1')
    b = cur.fetchone()[0]
    with open('s.jpg', 'wb') as f:
        f.write(b)
    print(b)
    coon.commit()
    coon.close()


if __name__ == '__main__':
    '''
    import chardet
    print chardet.detect(b'Hello, world!')
    '''
    main()