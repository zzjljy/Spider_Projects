# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy import Request, Spider
from urllib import parse
from urllib.parse import urlencode
from arcgis_tiles.items import ArcgisTilesJson, ArcgisTilesItem
from scrapy import Item, Field


class TilesSpider(scrapy.Spider):
    name = 'tiles'
    allowed_domains = ['61.240.19.180:6080']
    base_url = 'http://61.240.19.180:6080'
    start_urls = ['http://61.240.19.180:6080/arcgis/rest/services/']
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
        'resultOffset': 0,
        'f': 'pjson',
    }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, self.parse)
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
                    # yield Request(folder_link, callback=self.parse_folders, dont_filter=True)
                pass
        pass

    def parse_services(self, response):
        # 请求的url，为了和json拼接
        tile_base_url = response.request.url
        # tile services 的名称，对应数据库中的名称
        tile_name = response.meta.get('tile_name')
        print('tile_name：', tile_name)
        # / html / body / table[3] / tbody / tr / td / a[1] json
        json_text = response.xpath('//tr/td[@class="apiref"]/a[1]/text()').extract()[0]
        if json_text.strip() == 'JSON':
            a_link = response.xpath('//tr/td[@class="apiref"]/a[1]/@href').extract()[0]
            a_link = '?f=json'
            # tile 的services的json信息
            json_a_href = parse.urljoin(tile_base_url, a_link)
            # yield Request(json_a_href, callback=self.parse_json, meta={'tile_name': tile_name}, dont_filter=True)
        # fields 为了获取所有的fields的信息，先
        params = urlencode(self.data_count)
        fields_url = tile_base_url + '/0/query?'
        fields_count_url = tile_base_url + '/0/query?' + params
        yield Request(fields_count_url, callback=self.parse_fields_count, meta={'tile_name': tile_name,
                                                                          'fields_url': fields_url}, dont_filter=True)
        ul = response.xpath('//div[@class="rbody"]/ul/li/ul')
        # 进入service详情页带startTiles
        if ul:
            for li in ul:
                a_link = li.xpath('./li')

                start_tile = a_link.xpath('./a[1]/text()').extract()[0]
                if start_tile.strip() == 'Start Tile':
                    start_link = a_link.xpath('./a[1]/@href').extract()[0]
                    end_link = a_link.xpath('./a[2]/@href').extract()[0]
                    end_tile = a_link.xpath('./a[2]/text()').extract()[0]
                    level = int(start_link.split('/')[-3])
                    start_row = int(start_link.split('/')[-2])
                    start_col = int(start_link.split('/')[-1])
                    end_row = int(end_link.split('/')[-2])
                    end_col = int(end_link.split('/')[-1])
                    path = '/'.join(start_link.split('/')[:-3])
                    if level < 1:
                        for row in range(start_row, end_row+1):
                            for col in range(start_col, end_col+1):
                                base_path = path + '/' + str(level) + '/' + str(row) + '/' + str(col)
                                tile_url = self.base_url + base_path
                                # yield Request(tile_url, callback=self.parse_tile, meta={
                                #     'tile_name': tile_name,
                                #     'row': row,
                                #     'col': col,
                                #     'level': level
                                # }, dont_filter=True)
                else:
                    pass

        else:
            pass

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

    def parse_fields_count(self, response):
        print('进入数据count')
        tile_name = response.meta.get('tile_name')
        fields_url = response.meta.get('fields_url')
        field_json = json.loads(response.text)
        field_count = field_json.get('count')
        # 获取有多少条数据，如果有数据则可以获取条数，如果没有属性表，则None
        if field_count:
            # 有条数，json中添加layers
            count = int(field_count)
            nums = int(count/1000)
            for i in range(nums+1):
                if count == 1:
                    self.data_field['resultOffset'] = ''
                else:
                    self.data_field['resultOffset'] = 1000*i
                params = urlencode(self.data_field)
                # 获取所有字段的json的url
                field_url = fields_url + params
                yield Request(field_url, callback=self.parse_filed, meta={
                    'tile_name': tile_name
                }, dont_filter=True)

    def parse_filed(self, response):
        print('进入获取fields数据的页面')
        print(response.request.url)
        all_field_json = json.loads(response.text)
        fields = all_field_json.get('fields')
        print(fields)
        for item_field in fields:
            print(item_field)

