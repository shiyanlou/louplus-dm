# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import ShiyanlouItem


class GithubSpider(scrapy.Spider):
    name = 'github_next_page'
    allowed_domains = ['github.com']

    @property
    def start_urls(self):
        return ('https://github.com/shiyanlou?tab=repositories', )

    def parse(self, response):
        repos = response.xpath('//li[@itemprop="owns"]')
        for repo in repos:
            item = ShiyanlouItem()
            item['repo_name'] = repo.xpath(".//a[@itemprop='name codeRepository']/text()").extract_first().strip()
            item['update_time'] = repo.xpath(".//relative-time/@datetime").extract_first()

            yield item

        # 如果 Next 按钮没被禁用，那么表示有下一页
        spans = response.css('div.pagination span.disabled::text')
        if len(spans) == 0 or spans[-1].extract() != 'Next':
            next_url = response.css('div.paginate-container a:last-child::attr(href)').extract_first()
            yield response.follow(next_url, callback=self.parse)
