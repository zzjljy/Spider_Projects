# -*- coding: utf-8 -*-
import json
import scrapy
import urllib
import math
from scrapy import Request, Spider
from urllib import parse
from urllib.parse import urlencode
from arcgis_tiles.items import ArcgisTilesJson, ArcgisTilesItem, FieldTestItem, ArcgisFieldNameItem
from scrapy import Item, Field
from scrapy.loader import ItemLoader
from arcgis_tiles.geojson_to_wkt import geojson_to_wkt


class TilesSpider(scrapy.Spider):
    name = 'tiles'
    # allowed_domains = ['10.12.200.110:8000']
    # base_url = 'http://10.12.200.110:8000'
    # start_urls = ['http://10.12.200.110:8000/rest/services/DWG2000/MapServer']
    allowed_domains = ['61.240.19.180:6080']
    base_url = 'http://61.240.19.180:6080'
    start_urls = ['http://61.240.19.180:6080/arcgis/rest/services/JH/JHTG1017/MapServer']

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
            tile_name = urllib.parse.unquote(str(url).split('/')[-2])
            yield Request(url, self.parse_services, meta={'tile_name': tile_name})
        pass

    def parse(self, response):
        services = response.xpath('//div[@class="rbody"]/ul/li')
        for li in services:
            # print(li)
            # 通过text()可以取出内容的，且内容为 (MapServer)的直接是services,进去可以进行service页面\
            # 进入可以进行tile和json下载, folder取出来content为空
            content = li.xpath('./text()')
            if content:
                # services
                text = content.extract()[0]
                if text.strip() == '(MapServer)':
                    # 链接和text，text是layer名
                    a_link = li.xpath('./a/@href').extract()[0]
                    tile_name = a_text = '_'.join(li.xpath('./a/text()').extract()[0].split('/'))
                    a_href = self.base_url + a_link
                    # print(a_href, a_text)
                    yield Request(a_href, callback=self.parse_services, dont_filter=True, meta={'tile_name': tile_name})
                pass
            else:
                # folder
                folder_path = li.xpath('./a/@href').extract()[0]
                if folder_path:
                    folder_link = self.base_url + folder_path
                    yield Request(folder_link, callback=self.parse_folders, dont_filter=True)
                pass
        pass

    def parse_services(self, response):
        # 请求的url，为了和json拼接
        tile_base_url = response.request.url
        # tile services 的名称，对应数据库中的名称
        tile_name = response.meta.get('tile_name')
        print('tile_name：', tile_name)
        a_link = '?f=json'
        json_url = parse.urljoin(tile_base_url, a_link)
        yield Request(json_url, callback=self.parse_json_1, meta={'tile_name': tile_name}, dont_filter=True)
        # / html / body / table[3] / tbody / tr / td / a[1] json
        # json_text = response.xpath('//tr/td[@class="apiref"]/a[1]/text()').extract()[0]
        # if json_text.strip() == 'JSON':
        #     a_link = response.xpath('//tr/td[@class="apiref"]/a[1]/@href').extract()[0]
        #     a_link = '?f=json'
        #     # tile 的services的json信息
        #     json_a_href = parse.urljoin(tile_base_url, a_link)
        #     yield Request(json_a_href, callback=self.parse_json, meta={'tile_name': tile_name}, dont_filter=True)
        # fields 为了获取所有的fields的信息，先
        # params = urlencode(self.data_count)
        # fields_url = tile_base_url + '/0/query?'
        # fields_count_url = tile_base_url + '/0/query?' + params
        # yield Request(fields_count_url, callback=self.parse_fields_count, meta={'tile_name': tile_name,
        #                                                                   'fields_url': fields_url}, dont_filter=True)
        # layer_url = tile_base_url + '/layers'
        # yield Request(layer_url, callback=self.parse_layers, meta={'tile_name': tile_name,
        #                                                                   'mapserver_url': tile_base_url}, dont_filter=True)

        # ul = response.xpath('//div[@class="rbody"]/ul/li/ul')
        # # 进入service详情页带startTiles
        # if ul:
        #     for li in ul:
        #         a_link = li.xpath('./li')
        #
        #         start_tile = a_link.xpath('./a[1]/text()').extract()[0]
        #         if start_tile.strip() == 'Start Tile':
        #             start_link = a_link.xpath('./a[1]/@href').extract()[0]
        #             end_link = a_link.xpath('./a[2]/@href').extract()[0]
        #             end_tile = a_link.xpath('./a[2]/text()').extract()[0]
        #             level = int(start_link.split('/')[-3])
        #             start_row = int(start_link.split('/')[-2])
        #             start_col = int(start_link.split('/')[-1])
        #             end_row = int(end_link.split('/')[-2])
        #             end_col = int(end_link.split('/')[-1])
        #             path = '/'.join(start_link.split('/')[:-3])
        #             # if level < 3:
        #             for row in range(start_row, end_row+1):
        #                 for col in range(start_col, end_col+1):
        #                     base_path = path + '/' + str(level) + '/' + str(row) + '/' + str(col)
        #                     tile_url = self.base_url + base_path
        #                     yield Request(tile_url, callback=self.parse_tile, meta={
        #                         'tile_name': tile_name,
        #                         'row': row,
        #                         'col': col,
        #                         'level': level
        #                     }, dont_filter=True)
        #         else:
        #             pass

        # else:
        #     pass

    def parse_folders(self, response):
        print('folder页面进入')
        # /html/body/div/ul
        ul = response.xpath('//div[@class="rbody"]/ul/li')
        if ul:
            for li in ul:
                content = li.xpath('./text()').extract()[0]
                if content.strip() == '(MapServer)':
                    a_path = li.xpath('./a/@href').extract()[0]
                    service_name = a_text = '_'.join(li.xpath('./a/text()').extract()[0].split('/'))
                    service_url = self.base_url + a_path
                    if service_url != 'http://61.240.19.180:6080/arcgis/rest/services/JN/TJ_DZDT/MapServer':
                        yield Request(service_url, callback=self.parse_services, dont_filter=True,
                                       meta={'tile_name': service_name})
        pass

    def parse_json(self, response):
        # json信息的解析
        tile_name = response.meta.get('tile_name')
        print('进入json页面', tile_name)
        tile_json = response.text
        tile_item = ArcgisTilesJson()
        tile_item['service_name'] = tile_name
        tile_item['service_config'] = tile_json
        yield tile_item
        pass

    def parse_json_1(self, response):
        # json信息的解析
        tile_name = response.meta.get('tile_name')
        base_url = response.request.url[:-7]
        print('进入json页面', tile_name)
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
        info = {
            2000000: 529.16772500211675,
            1000000: 264.58386250105838,
            500000: 132.29193125052919,
            250000: 66.145965625264594,
            125000: 33.072982812632297,
            64000: 16.933367200067735,
            32000: 8.4666836000338677,
            16000: 4.2333418000169338,
            8000: 2.1166709000084669,
            5000: 1.3229193125052918,
            4000: 1.0583354500042335,
            3000: 0.79375158750317509,
            2000: 0.52916772500211673,
            1000: 0.26458386250105836,
            500: 0.13229193125052918,
            250: 0.066145965625264591
        }
        for level_resolution_scale in level_resolution:
            level = level_resolution_scale.get('level')
            # resolution = level_resolution_scale.get('resolution')
            scale = level_resolution_scale.get('scale')
            # resolution = scale * 0.0254000508 / 96
            resolution = info.get(scale)
            if not resolution:
                resolution = level_resolution_scale.get('resolution')
            # resolution = level_resolution_scale.get('resolution')
            img_meter = resolution * 256
            start_col = (xmin - origin_x) / resolution / 256
            end_col = (xmax - origin_x) / resolution / 256
            start_row = (origin_y - ymax) / resolution / 256
            end_row = (origin_y - ymin) / resolution / 256
            print('row,col,level', level, start_row, start_col, end_row, end_col)
            for row in range(int(start_row)-1, math.ceil(end_row)+1):
                for col in range(int(start_col)-1, math.ceil(end_col)+1):
                    # if level < 6:
                    tile_url = base_url + '/tile' + '/' + str(level) + '/' + str(row) + '/' + str(col)
                    # tile_url = self.base_url + base_path
                    yield Request(tile_url, callback=self.parse_tile, meta={
                        'tile_name': tile_name,
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
            tile_name = response.meta.get('tile_name')
            tile_content = response.body
            item_tile['tile_collection'] = tile_name
            item_tile['x'] = row
            item_tile['y'] = col
            item_tile['z'] = level
            item_tile['image'] = tile_content
            yield item_tile
        pass

    def parse_layers(self, response):
        # 解析有多少层，对应多少个数据表
        print('进入layers页面')
        tile_name = response.meta.get('tile_name')
        laysers_ul = response.xpath('//div[@class="rbody"]/ul')
        params = urlencode(self.data_count)
        for layser_ul in laysers_ul:
            layer_path = layser_ul.xpath('./h3/a/@href').extract()[0]
            # layer_level = layser_ul.xpath('./h3/text()').extract()[1].strip()[1:-1]
            service_name = tile_name
            layer_name = tile_name+'_'+layser_ul.xpath('./h3/a/text()').extract()[0]+'_'+layser_ul.xpath('./h3/text()').extract()[1].strip()[1:-1]
            # layer_name = tile_name+layser_ul.xpath('./h3/a/text()').extract()[0]+layser_ul.xpath('./h3/text()').extract()[1]
            fields_url = self.base_url+layer_path + '/query?'
            layer_url = self.base_url+layer_path + '/query?' + params
            yield Request(layer_url, callback=self.parse_fields_count, meta={'tile_name': layer_name, 'service_name':
                          service_name, 'fields_url': fields_url}, dont_filter=True)

        pass

    def parse_fields_count(self, response):
        tile_name = response.meta.get('tile_name')
        service_name = response.meta.get('service_name')
        fields_url = response.meta.get('fields_url')
        field_json = json.loads(response.text)
        field_count = field_json.get('count')
        # 获取有多少条数据，如果有数据则可以获取条数，如果没有属性表，则None
        if field_count:
            # 有条数，json中添加layers
            count = int(field_count)
            print('count数据条数：', count, tile_name)
            nums = int(count/1000)
            for i in range(nums+1):
                if i == 0:
                    self.data_field['resultOffset'] = ''
                else:
                    self.data_field['resultOffset'] = 1000*i
                params = urlencode(self.data_field)
                # 获取所有字段的json的url
                field_url = fields_url + params
                yield Request(field_url, callback=self.parse_filed, meta={
                    'tile_name': tile_name, 'service_name': service_name
                }, dont_filter=True)

    def parse_filed(self, response):
        print('进入获取fields数据的页面', response.meta.get('tile_name'))
        layer_item = ArcgisFieldNameItem()
        item = Item()
        layer_name = response.meta.get('tile_name')
        service_name = response.meta.get('service_name')
        layer_item['service_name'] = service_name
        layer_item['layers'] = layer_name
        yield layer_item
        all_field_json = json.loads(response.text)
        if not all_field_json.get('error'):
            # 获取wkid
            wkid = 0
            wkid = all_field_json.get('spatialReference').get('wkid')

            # 所有的字段
            fields_info = all_field_json.get('fields')
            print(layer_name, 'fields', fields_info)
            item.fields['layer_name'] = Field()
            item['layer_name'] = layer_name
            item.fields['create_table_info'] = Field()
            item.fields['geom'] = Field()
            # create_table_info = '''create table if not exists %s(id int primary key AUTOINCREMENT,''' % layer_name
            create_table_info = '''create table if not exists %s(''' % layer_name
            for field in fields_info:
                # item.fields[field.get('name')] = Field()
                field_name = field.get('name') + ' '
                field_type = field.get('type')
                if field_type == 'esriFieldTypeOID':
                    field_type = 'integer'
                elif field_type == 'esriFieldTypeInteger':
                    field_type = 'integer'
                elif field_type == 'esriFieldTypeSmallInteger':
                    field_type = 'integer'
                elif field_type == 'esriFieldTypeString':
                    field_type = 'character varying(254)'
                elif field_type == 'esriFieldTypeDouble':
                    field_type = 'numeric'
                else:
                    field_type = 'character varying(254)'
                create_table_info += field_name
                create_table_info += field_type
                create_table_info += ','
            create_table_info += 'geom geometry'
            create_table_info += ')'
            item['create_table_info'] = create_table_info
            features = all_field_json.get('features')
            if features:
                for feature_item in features:
                    attributes = feature_item.get('attributes')
                    if attributes:
                        for k, v in attributes.items():
                            item.fields[k] = Field()
                            item[k] = v

                    geometry = feature_item.get('geometry')
                    geo_wkt = geojson_to_wkt(geometry)
                    geom_from_ewkt = 'SRID=%s;%s' % (wkid, geo_wkt)
                    # print(geom_from_ewkt)
                    item['geom'] = geom_from_ewkt

                    yield item
