#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @File : sqlite3_test.py
    @Author: LiJiaoyang
    @Date : 2020/5/14
    @Desc : 
'''
import sqlite3

dblocation = r'D:\zl_datas\data_database\Sqlite\Spider_teste.sqlite3'
coon = sqlite3.connect(dblocation)
cur = coon.cursor()
table_name = 'spider_05122'
# print(cur.execute("select * from ({})".format(table_name)).fetchone())
cur.execute("create table {}(id primary key not null)".format(table_name))