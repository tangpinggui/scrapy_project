# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule



class CfSpider(CrawlSpider):
    def __init__(self):
        super().__init__()
        self.count=0
    name = 'cf'
    allowed_domains = ['circ.gov.cn']
    start_urls = ['http://circ.gov.cn/web/site0/tab5240/']
    # 提取规则 follow=True 继续提取（提取下一页地址 需要True）
    rules = (
        # /web/site0/tab5240/info4136797.htm
        Rule(LinkExtractor(allow=r'/web/site0/tab5240/info\d*\.htm'), callback='parse_item'),
        # /web/site0/tab5240/module14430/page2.htm   http://circ.gov.cn/web/site0/tab5240/module14430/page2.htm
        # follow 当前url地址的响应是重新通过rules提取的的url地址
        Rule(LinkExtractor(allow=r'/web/site0/tab5240/module14430/page\d+\.htm'), follow=True),
    )

    def parse_item(self, response):
        self.count += 1
        item = {}
        item['title'] = re.findall('<!--TitleStart-->(.*)<!--TitleEnd-->', response.body.decode())[0]
        item['pub_date'] = re.findall('发布时间：(20\d{2}-\d{2}-\d{2})', response.body.decode())[0]
        # print('第%s条' %self.count)
        yield item
