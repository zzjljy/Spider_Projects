# -*- coding: utf-8 -*-
import scrapy


class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/get']

    def parse(self, response):
        # 可以看到headers
        self.logger.debug(response.text)
        self.logger.debug('status code:'+str(response.status))
        pass
