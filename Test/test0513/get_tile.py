#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @File : get_tile.py
    @Author: LiJiaoyang
    @Date : 2020/5/13
    @Desc :基本功能实现了，下载速度比较慢
'''

import requests
from urllib import parse
import os
from bs4 import BeautifulSoup
import re
import sqlite3


dblocation = r'D:\zl_datas\data_database\Sqlite\Spider_teste.sqlite3'
coon = sqlite3.connect(dblocation)
cur = coon.cursor()


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'
}
# 加上这句话fiddler可以抓到请求包
proxies = {'http': 'http://localhost:8888', 'https':'http://localhost:8888'}


def get_main_page(url):
    domin = parse.urlparse(url)
    print(domin)
    scheme = domin.scheme
    netloc = domin.netloc
    # print(dir(domin))
    # netloc是需要拼接的， hostname不带端口号
    print('netloc', domin.netloc)
    print('scheme', domin.scheme)
    # print('hostname', domin.hostname)
    # print('port', domin.port)
    req = requests.get(url, headers=headers, proxies=proxies)
    html_encoding = req.encoding
    print('编码方式为：', html_encoding)
    if req.status_code == 200:
        return req, netloc, scheme
    else:
        return None, 0, 0
    pass


def get_services(url):
    # folders和services页面
    html, netloc, schme = get_main_page(url)
    soup = BeautifulSoup(html.text, 'lxml')
    # print(soup.prettify())
    if html:
        for ul in soup.select('.rbody>ul'):
            # 获取两个ul中的内容，一个folders，一个services
            for item in ul.select('li>a'):
                print('------------------------------------')
                print('链接显示内容:', item.get_text())
                path = item['href']
                data = [schme, netloc, path, '', '', '']
                a_href = parse.urlunparse(data)

                if re.findall(r'(^.*?MapServer$)', str(a_href)) or re.findall(r'(^.*?MapServer/$)', str(a_href)):
                    if item.get_text() != 'beijing_0514':
                        create_table(item.get_text())
                        print('server详情链接：', a_href)
                        get_detail_page(a_href, item.get_text())
                # my_str = 'MapServer'
                # if re.findall(my_str, str(a_href)):
                #     print('符合条件')


def get_detail_page(url, table):
    '''
    进入每个server的详情页，爬取瓦片和json信息
    :param url:
    :return:
    '''
    # data = [schme, netloc, path, '', '', '']
    html, netloc, scheme = get_main_page(url)
    if html:
        soup = BeautifulSoup(html.text, 'lxml')
        for ul in soup.select('.rbody>ul>li>ul'):
            start_row = 0
            start_col = 0
            end_row = 0
            end_col = 0
            level = 0
            href_prefix = []
            for item in ul.select('li>a'):
                print('href:', item)
                path = item['href']
                data = [scheme, netloc, path, '', '', '']
                detail_href = parse.urlunparse(data)
                print('detail_href', detail_href)
                # 判断详情链接是否是瓦片的链接
                if re.findall(r'(^.*?MapServer/tile/(\d{1,})/(\d{1,})/(\d{1,})$)', str(detail_href)):
                    print('符合条件的链接', detail_href)
                    href_prefix = str(detail_href).split('/')[:-3]
                    print(str(detail_href).split('/')[:-3])
                    text = item.get_text()
                    level = int(str(detail_href).split('/')[-3])
                    if text == 'Start Tile':
                        start_row = int(str(detail_href).split('/')[-2])
                        start_col = int(str(detail_href).split('/')[-1])
                    elif text == 'End Tile':
                        end_row = int(str(detail_href).split('/')[-2])
                        end_col = int(str(detail_href).split('/')[-1])
                    else:
                        pass
            print('行列：', start_row, start_col, end_row, end_col, level)
            if start_row == 0 and start_col == 0 and end_row == 0 and end_col == 0:
                pass
            else:
                get_tile(href_prefix, start_row, start_col, end_row, end_col, level, table)


def get_tile(url, start_row, start_col, end_row, end_col, level, table):
    '''
    获取每一张瓦片
    :param url:
    :param start_row:
    :param start_col:
    :param end_row:
    :param end_col:
    :param level:
    :return:
    '''
    url_prefix = '/'.join(url)
    print('前缀链接：', url_prefix)
    for row in range(start_row, end_row+1):
        for col in range(start_col, end_col+1):
            tile_href = url_prefix+'/'+str(level)+'/'+str(row)+'/'+str(col)
            print(tile_href)
            html, netloc, scheme = get_main_page(tile_href)
            if html:
                image = html.content
                insert_into_sqlite(table, row, col, level, image)


def create_table(table_name):
    '''
    创建sqlite表
    :param table_name:
    :return:
    '''
    # sql = "create table IF NOT EXISTS ({})(id integer primary key not null authorization ,row integer , col integer , level integer ,image blob)"
    cur.execute("create table {}(id integer primary key AUTOINCREMENT,row integer , col integer , level integer ,image blob)".format(table_name))
    coon.commit()
    print('表创建成功')


def insert_into_sqlite(table, row, col, level, image):
    '''
    将瓦片的二进制存入sqlite中
    :param table:
    :param row:
    :param col:
    :param level:
    :param image:
    :return:
    '''

    cur.execute("insert into {}(row, col, level, image) values (?, ?, ?, ?)".format(table), (row, col, level, image))
    coon.commit()


if __name__ == '__main__':

    url = 'http://61.240.19.180:6080/arcgis/rest/services/'
    get_services(url)
    coon.close()
    # get_main_page(url)
