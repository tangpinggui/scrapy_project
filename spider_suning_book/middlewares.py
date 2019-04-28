# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random


class RandomUAMiddleware:
    def process_request(self, request, spider):
        # 随机选择ua
        ua = random.choice(spider.settings.get('USER_AGENT_LIST'))
        request.headers["User-Agent"] = ua


class CheckUserAgent:
    def process_response(self, request, response, spider):
        # 打印ua
        print(request.headers['User-Agent'])
        return response


class ProxyMiddleware:
    def process_request(self, request, spider):
        # 添加代理(选择随机代理)
        request.meta["proxy"] = "http://124.115.126.76:808"