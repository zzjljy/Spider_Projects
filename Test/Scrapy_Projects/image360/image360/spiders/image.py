# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy import Spider, Request
from urllib.parse import urlencode
from image360.items import ImageItem
# https://image.so.com/zjl?ch=photography&sn=60&listtype=new&temp=1

class ImageSpider(scrapy.Spider):
    name = 'image'
    allowed_domains = ['images.so.com']
    start_urls = ['http://images.so.com/']

    def start_requests(self):
        data = {'ch': 'photography', 'listtype': 'new'}
        base_url = 'https://image.so.com/zjl?'
        for page in range(1, self.settings.get('MAX_PAGE') + 1):
            data['sn'] = page * 30
            # urlencode将字典转化为URL的GET参数
            params = urlencode(data)
            url = base_url + params
            yield Request(url, self.parse)

    def parse(self, response):
        result = json.loads(response.text)
        if result.get('count') > 0:
            for image in result.get('list'):
                item = ImageItem()
                item['id'] = image.get('id')
                item['url'] = image.get('qhimg_url')
                item['title'] = image.get('title')
                item['thumb'] = image.get('qhimg_thumb')
                yield item
        pass
