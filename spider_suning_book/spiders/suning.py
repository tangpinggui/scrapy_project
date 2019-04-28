# -*- coding: utf-8 -*-
import scrapy

from spider_suning_book.items import SpiderSuningBookItem
from copy import deepcopy


class SuningSpider(scrapy.Spider):
    name = 'suning'
    allowed_domains = ['suning.com']
    # start_urls = ['http://list.suning.com/0-502282-0.html?safp=d488778a.10004.0.47cb7a84d7']
    start_urls = ['http://list.suning.com/0-502282-0.html']

    def parse(self, response):
        # 图书分类
        item = SpiderSuningBookItem()
        li_category = response.xpath("//a[@class='r-name']")[0]
        print(li_category)
        # for li in li_category:
        #     item['category'] = li.xpath("./@title").extract_first()
        #     item['category_detail_href'] = 'http:' + li.xpath("./@href").extract_first()
        #     yield scrapy.Request(
        #         url=item['category_detail_href'],
        #         callback=self.category_detaile_parse,
        #         meta={'item': deepcopy(item)}
        #     )
        item['category'] = li_category.xpath("./@title").extract_first()
        item['category_detail_href'] = 'http:' + li_category.xpath("./@href").extract_first()
        yield scrapy.Request(
            url=item['category_detail_href'],
            callback=self.category_detaile_parse,
            meta={'item': deepcopy(item)}
        )

    def category_detaile_parse(self, response):
        # 图书信息
        item = response.meta['item']

        li_category = response.xpath("//div[@class='res-info']")
        item['name'] = []
        for li in li_category:
            # item['name'] = li.xpath("./div[2]/a/@title").extract_first()
            item['name'].append(li.xpath("./div[@class='title-selling-point']/a/text()").extract_first().replace('\n', ''))
        print(item)
        yield item
