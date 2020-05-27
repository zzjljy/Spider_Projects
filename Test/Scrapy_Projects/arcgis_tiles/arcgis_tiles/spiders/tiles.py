# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy import Request, Spider
from urllib import parse
from arcgis_tiles.items import ArcgisTilesJson


class TilesSpider(scrapy.Spider):
    name = 'tiles'
    allowed_domains = ['61.240.19.180:6080']
    base_url = 'http://61.240.19.180:6080'
    start_urls = ['http://61.240.19.180:6080/arcgis/rest/services/']
    scheme = 'http'

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, self.parse)
        pass

    def parse(self, response):
        # self.logger.debug(response)
        # result = response.text
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
                    tile_name = a_text = li.xpath('./a/text()').extract()[0]
                    a_href = self.base_url + a_link
                    # print(a_href, a_text)
                    yield Request(a_href, callback=self.parse_services, dont_filter=True, meta={'tile_name': tile_name})
                pass
            else:
                # folder
                pass
        pass

    def parse_services(self, response):
        print('进入services页面')
        # 请求的url，为了和json拼接
        tile_base_url = response.request.url
        # tile services 的名称，对应数据库中的名称
        tile_name = response.meta.get('tile_name')
        print('tile_name：', tile_name)
        # / html / body / table[3] / tbody / tr / td / a[1]
        json_text = response.xpath('//tr/td[@class="apiref"]/a[1]/text()').extract()[0]
        if json_text.strip() == 'JSON':
            a_link = response.xpath('//tr/td[@class="apiref"]/a[1]/@href').extract()[0]
            a_link = '?f=json'
            # tile 的services的json信息
            json_a_href = parse.urljoin(tile_base_url, a_link)
            # yield Request(json_a_href, callback=self.parse_json, meta={'tile_name': tile_name}, dont_filter=True)
        # /html/body/div/ul[2]/li[4]/ul[1]/li
        ul = response.xpath('/html/body/dic[@class="rbody"]/ul/li/ul/li')
        for li in ul:
            print(li)
        pass

    def parse_folders(self, response):
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
