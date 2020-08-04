# -*- coding: utf-8 -*-
import json
import scrapy
import urllib
import math
import copy
from scrapy import Request, Spider
from urllib import parse
from urllib.parse import urlencode
from arcgis_tiles.items import ArcgisTilesJson, ArcgisTilesItem, FieldTestItem, ArcgisFieldNameItem
from scrapy import Item, Field
from scrapy.loader import ItemLoader
from arcgis_tiles.geojson_to_wkt import geojson_to_wkt

tile_name = 'DWG20002'


class TilesSpider(scrapy.Spider):
    name = 'tiles'
    allowed_domains = ['10.12.200.110:8000']
    base_url = 'http://10.12.200.110:8000'
    start_urls = ['http://10.12.200.110:8000/rest/services/DWG2000/MapServer']
    # allowed_domains = ['61.240.19.180:6080']
    # base_url = 'http://61.240.19.180:6080'
    # start_urls = ['http://61.240.19.180:6080/arcgis/rest/services/JH/JHYX0910/MapServer']

    scheme = 'http'
    data_count = {
        'where': '1=1',
        'geometryType': 'esriGeometryEnvelope',
        'spatialRel': 'esriSpatialRelIntersects',
        'returnGeometry': 'true',
        'returnTrueCurves': 'false',
        'returnIdsOnly': 'false',
        'returnCountOnly': 'true',
        'returnDistinctValues': 'false',
        'f': 'pjson',
    }
    data_field = {
        'where': '1=1',
        'geometryType': 'esriGeometryEnvelope',
        'spatialRel': 'esriSpatialRelIntersects',
        'outFields': '*',
        'returnGeometry': 'true',
        'returnTrueCurves': 'false',
        'returnIdsOnly': 'false',
        'returnCountOnly': 'false',
        'returnDistinctValues': 'false',
        'resultOffset': 1,
        'f': 'pjson',
    }

    def start_requests(self):
        for url in self.start_urls:
            # tile_name = urllib.parse.unquote(str(url).split('/')[-2])
            yield Request(url, self.parse_services)
        pass

    def parse_services(self, response):
        # 请求的url，为了和json拼接
        tile_base_url = response.request.url
        a_link = '?f=json'
        json_url = parse.urljoin(tile_base_url, a_link)
        yield Request(json_url, callback=self.parse_json_1, dont_filter=True)

    def parse_json_1(self, response):
        # json信息的解析
        # meta = copy.copy(response.meta)
        # tile_name = meta.get('tile_name')
        base_url = response.request.url[:-7]
        tile_json = response.text
        tile_json = json.loads(tile_json)
        origin = tile_json.get('tileInfo').get('origin')
        origin_x = origin.get('x')
        origin_y = origin.get('y')
        level_resolution = tile_json.get('tileInfo').get('lods')
        initia = tile_json.get('fullExtent')
        full = tile_json.get('initialExtent')
        if not initia:
            initia = tile_json.get('initialExtent')
        xmin = initia.get('xmin')
        ymin = initia.get('ymin')
        xmax = initia.get('xmax')
        ymax = initia.get('ymax')
        for level_resolution_scale in level_resolution:
            level = level_resolution_scale.get('level')
            resolution = level_resolution_scale.get('resolution')
            scale = level_resolution_scale.get('scale')
            # resolution = scale * 0.0254000508 / 96
            # resolution = info.get(scale)
            if not resolution:
                resolution = level_resolution_scale.get('resolution')
            # resolution = level_resolution_scale.get('resolution')
            start_col = (xmin - origin_x) / resolution / 256
            end_col = (xmax - origin_x) / resolution / 256
            start_row = (origin_y - ymax) / resolution / 256
            end_row = (origin_y - ymin) / resolution / 256
            print('row,col,level', level, start_row, start_col, end_row, end_col)
            for row in range(int(start_row), math.ceil(end_row) + 1):
                for col in range(int(start_col), math.ceil(end_col) + 1):
                    # tile_name = meta.get('tile_name')
                    level = copy.copy(level)
                    # if level < 4:
                    tile_url = base_url + '/tile' + '/' + str(level) + '/' + str(row) + '/' + str(col)
                    # tile_url = self.base_url + base_path
                    yield Request(tile_url, callback=self.parse_tile, meta={
                        # 'tile_name': tile_name,
                        'row': row,
                        'col': col,
                        'level': level
                    }, dont_filter=True)

    def parse_tile(self, response):
        # 瓦片解析
        status_code = response.status
        if status_code == 200:
            item_tile = ArcgisTilesItem()
            level = response.meta.get('level')
            row = response.meta.get('row')
            col = response.meta.get('col')
            # tile_name = response.meta.get('tile_name')
            tile_content = response.body
            item_tile['tile_collection'] = tile_name
            item_tile['x'] = row
            item_tile['y'] = col
            item_tile['z'] = level
            item_tile['image'] = tile_content
            yield item_tile
        pass
