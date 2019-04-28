# -*- coding: utf-8 -*-
import scrapy
import re

# 模拟人人网网登陆
class Renren1Spider(scrapy.Spider):
    name = 'renren1'
    allowed_domains = ['renren.com']
    start_urls = ['http://renren.com']
    """
    email: 18781736136
    icode: 
    origURL: http://www.renren.com/970578188/profile?v=info_timeline
    domain: renren.com
    key_id: 1
    captcha_type: web_login
    password: 6af626fe325aa7fcea5e6ff3c541404d9104667d6d941a5c5c30390c2d5da8ad
    rkey: 86cfb8063d4b47d05407cc549819f975
    f: 
    """
    # func 1
    def parse(self, response):
        origURL = response.xpath("//input[@name='origURL']/@value").extract_first()
        domain = 'renren.com'
        key_id = response.xpath("//input[@name='key_id']/@value").extract_first()
        captcha_type = response.xpath("//input[@name='captcha_type']/@value").extract_first()
        # rkey = response.xpath("//input[@name='rkey']/@value").extract_first()
        post_data = dict(
            email='18781736136',
            password='wcjkgshdh123',
            origURL=origURL,
            domain=domain,
            key_id=key_id,
            captcha_type=captcha_type,
            # rkey='', #不知道怎么获取,貌似不要也能登录
            f=''
        )
        yield scrapy.FormRequest(
            url="http://www.renren.com/PLogin.do",
            formdata=post_data,
            callback=self.after_login
        )
    # func 2
    # def parse(self, response):
    #     post_data = dict(
    #         email='18781736136',
    #         password='wcjkgshdh123',
    #     )
    #     yield scrapy.FormRequest.from_response(
    #         response, # 自动从response找到form表单中
    #         formdata=post_data,
    #         callback=self.after_login
    #     )


    def after_login(self, response):
        print('start....')
        with open('renren.html', 'w') as f:
            f.write(response.body.decode())
