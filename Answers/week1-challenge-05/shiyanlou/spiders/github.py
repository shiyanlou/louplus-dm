# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import ShiyanlouItem


class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']

    @property
    def start_urls(self):
        url_temp = 'https://github.com/shiyanlou?after={}&tab=repositories'
        # 此参考会失效，请自行重新手动复制 after 参数
        after = [
            '',
            'Y3Vyc29yOnYyOpK5MjAxNy0wNi0wN1QwNjoxOTo1NyswODowMM4FkpYw',
            'Y3Vyc29yOnYyOpK5MjAxNS0wMS0yNVQxMTozMTowNyswODowMM4Bxrsx',
            'Y3Vyc29yOnYyOpK5MjAxNC0xMS0yMFQxMzowMzo1MiswODowMM4BjkvL',
        ]
        return (url_temp.format(i) for i in after) # 1-4 页

    def parse(self, response):
        repos = response.xpath('//li[@itemprop="owns"]')
        for repo in repos:
            item = ShiyanlouItem()
            item['repo_name'] = repo.xpath(".//a[@itemprop='name codeRepository']/text()").extract_first().strip()
            item['update_time'] = repo.xpath(".//relative-time/@datetime").extract_first()
            
            yield item