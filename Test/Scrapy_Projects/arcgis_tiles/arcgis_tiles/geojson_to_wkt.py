#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @File : geojson_to_wkt.py
    @Author: LiJiaoyang
    @Date : 2020/6/4
    @Desc : 
'''
from geodaisy import converters


def geojson_to_wkt(geojson):
    '''
    将geojson转为wkt形式，转为数据
    :param geojson:
    :return:
    '''
    geometry = geojson
    geo_json = dict()
    if geometry.get('rings'):
        geo_type = 'MultiPolygon'
        geo_json['type'] = geo_type
        geo_json['coordinates'] = geometry.get('rings')
    elif geometry.get('paths'):
        geo_type = 'MultiLineString'
        geo_json['type'] = geo_type
        geo_json['coordinates'] = geometry.get('paths')
    elif geometry.get('x'):
        geo_type = 'Point'
        geo_json['type'] = geo_type
        geo_json['coordinates'] = [geometry.get('x'), geometry.get('y')]
    else:
        geo_type = 'MultiPoint'
        geo_json['type'] = geo_type
        geo_json['coordinates'] = [geometry.get('x'), geometry.get('y')]

    geo_wkt = converters.geojson_to_wkt(geo_json)
    return geo_wkt

