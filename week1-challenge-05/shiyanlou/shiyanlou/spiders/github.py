# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import ShiyanlouItem

"""
手动获取下一页爬虫
"""

class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']

    @property
    def start_urls(self):
        url_temp = 'https://github.com/shiyanlou?after={}&tab=repositories'
        after = [
            '',
            'Y3Vyc29yOnYyOpK5MjAxNy0wNi0wNlQxNzozNjoxNSswODowMM4FkpW2',
            'Y3Vyc29yOnYyOpK5MjAxNS0wMS0yM1QxNDoxODoyMSswODowMM4By2VI',
            'Y3Vyc29yOnYyOpK5MjAxNC0xMS0xOVQxMDoxMDoyMyswODowMM4BmcsV',
        ]
        return (url_temp.format(i) for i in after) # 1-4 页

    def parse(self, response):
        repos = response.xpath('//li[@itemprop="owns"]')
        for repo in repos:
            item = ShiyanlouItem()
            item['repo_name'] = repo.xpath("./div/h3/a/text()").extract_first().strip()
            item['update_time'] = repo.xpath("./div/relative-time/@datetime").extract_first()
            
            yield item