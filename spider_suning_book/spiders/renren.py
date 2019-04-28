# -*- coding: utf-8 -*-
import re
import scrapy


class RenrenSpider(scrapy.Spider):
    name = 'renren'
    allowed_domains = ['renren.com']
    start_urls = ['http://renren.com/']

    def start_requests(self):
        cookies = 'anonymid=juzai6na-g0fmvf; depovince=GW; _r01_=1; ick_login=9de0dec9-4f94-42e0-819b-22df9e9adf66; ick=75ca63f4-c056-4af0-ba6e-7683bb07d04d; jebecookies=747a7092-f53c-40ae-bc0b-90b3f9ab5e2d|||||; JSESSIONID=abcjUmG7wh1SragUBfEPw; _de=8B28AA93122391F898B641D1F469956B; p=9984be9e31957abbf89e6751ad2fd8f48; first_login_flag=1; ln_uact=18781736136; ln_hurl=http://head.xiaonei.com/photos/0/0/men_main.gif; t=59071958da717542e6a80ffd0df189c38; societyguester=59071958da717542e6a80ffd0df189c38; id=970578188; xnsid=a1ea20ee; ver=7.0; loginfrom=null; jebe_key=ed626104-9dc0-45aa-961c-2cfea0e1935d%7C570ae1432b36360003bbd95b7fb6661a%7C1556356655118%7C1%7C1556356654129; wp_fold=0; XNESSESSIONID=2d1bc0ef1740; vip=1'
        cookies = {i.split('=')[0]: i.split('=')[1] for i in cookies.split('; ')}
        start_urls = ['http://www.renren.com/970578188/profile?v=info_timeline']
        yield scrapy.Request(
            start_urls[0],
            callback=self.parse_detail,
            cookies=cookies
        )

    def parse_detail(self, response):
        res = response.xpath("//div[@class='love-infobox']/p/text()").extract_first()
        print(res)
        # print(re.findall(r'单身', response.body.decode()))
