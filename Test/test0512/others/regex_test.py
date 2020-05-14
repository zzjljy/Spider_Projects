#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @File : regex_test.py
    @Author: LiJiaoyang
    @Date : 2020/5/13
    @Desc : 
'''

import re
#测试文本
msg1 = "goodgoodstudy!,dooodooooup"
#匹配单词o出现0次或者多次的情况
print(re.findall(r"o*",msg1))
# 匹配一段字符串中出现单词o字符1次或者多次的情况
print(re.findall(r"o+",msg1))
# 匹配一段字符串中出现单词o字符0次或者1次的情况
print(re.findall(r"o?",msg1))
# 匹配字符串中连续出现2次字符o的情况
print(re.findall(r"o{2}",msg1))
# 匹配字符串中连续出现2次以上字符o的情况
print(re.findall(r"o{2,}",msg1))
# 匹配字符串中连续出现2次以上3次以内字符o的情况
print(re.findall(r"o{2,3}",msg1))
