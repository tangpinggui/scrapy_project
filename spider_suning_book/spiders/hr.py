# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class HrSpider(CrawlSpider):
    name = 'hr'
    allowed_domains = ['tencent.com']
    start_urls = ['https://hr.tencent.com/index.php']
    rules = (
        # https://hr.tencent.com/social.php
        Rule(LinkExtractor(allow=r'https://hr.tencent.com/position.php'),
             callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'https://hr.tencent.com/position.php?keywords=&tid=0&start=\d{1}0#a'),
             follow=True),
    )

    def parse_item(self, response):
        item = {}
        tr_list = response.xpath("//table[@class='tablelist']/tr")[1:-1]
        for tr in tr_list:
            item['title'] = tr.xpath("./td[1]/a/text()").extract_first()
            item['position'] = tr.xpath("./td[2]/text()").extract_first()
            item['pub_date'] = tr.xpath("./td[5]/text()").extract_first()
            yield item