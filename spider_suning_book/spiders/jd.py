# -*- coding: utf-8 -*-
import scrapy
import urllib
import json
from copy import deepcopy


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com', 'p.3.cn']
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        # 大分类
        dt_list = response.xpath("//div[@class='mc']/dl/dt")
        for dt in dt_list:
            item = {}
            item['b_cate_name'] = dt.xpath("./a/text()").extract_first() # 大分类名字
            # 小分类
            dd_list = dt.xpath("./following-sibling::dd[1]")
            for dd in dd_list:
                item['s_cate_name'] = dd.xpath("./em/a/text()").extract_first() # 小分类名字
                item['s_cate_url'] = dd.xpath("./em/a/@href").extract_first() # 小分类url
                if item['s_cate_url'] is not None:
                    item['s_cate_url'] = urllib.parse.urljoin(response.url, item['s_cate_url'])
                    yield scrapy.Request(
                        item['s_cate_url'],
                        callback=self.parse_book_list,
                        meta={'item': deepcopy(item)}
                    )

    def parse_book_list(self, response):
        item = response.meta['item']
        book_list = response.xpath("//li[@class='gl-item']") # 小分类中的书
        for book in book_list:
            item['book_buy_url'] = book.xpath(".//div[@class='p-img']/a/@href").extract_first()
            if item['book_buy_url'] is not None:
                item['book_buy_url'] = urllib.parse.urljoin(response.url, item['book_buy_url'])
            item['book_img_url'] = book.xpath(".//div[@class='p-img']/a/img/@src").extract_first()
            if item['book_img_url'] is None:
                item['book_img_url'] = book.xpath(".//div[@class='p-img']/a/img/@data-lazy-img").extract_first()
            item['book_name'] = book.xpath(".//div[@class='p-name']/a/em/text()").extract_first().strip()
            item['book_author'] = book.xpath(".//span[@class='author_type_1']/a/text()").extract()
            item['skuIds'] = book.xpath(".//div/@data-sku").extract_first()
            yield scrapy.Request(
                'https://p.3.cn/prices/mgets?skuIds=J_{}'.format(item['skuIds']),
                callback=self.parse_book_price,
                meta={'item': deepcopy(item)}
            )

        # 小分类 下一页
        next_url = response.xpath("//a[@class='pn-next']/@href").extract_first()
        if next_url is not None:
            next_url = urllib.parse.urljoin(response.url, next_url)
            yield scrapy.Request(
                next_url,
                callback=self.parse_book_list,
                meta={'item': item}
            )

    def parse_book_price(self, response):
        item = response.meta['item']
        item['book_price'] = json.loads(response.body.decode())[0]['op']
        print(item)
        yield item