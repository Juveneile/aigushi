# -*- coding: utf-8 -*-
"""
爬取好故事，哈哈
"""
import scrapy
from aigushi.items import AigushiItem


class AigushiSpiderSpider(scrapy.Spider):
    name = 'aigushi_spider'
    allowed_domains = ['www.5aigushi.com']
    # 这里先爬取爱情小说
    start_urls = ['http://www.5aigushi.com/aiqing']

    # 默认解析方式
    def parse(self, response):
        # 先获取第一页的小说名称
        story_list = response.xpath('//div[@class="listbox1"]/ul[@class="e2"]/li')
        for i_item in story_list:
            aigushi_item = AigushiItem()
            aigushi_item['story_name'] = i_item.xpath('.//a[@target="_blank"and@class="title"]/text()').extract_first()
            # 获取正文的链接
            body_link = 'http://www.5aigushi.com/' + i_item.xpath('.//p//a[@class="t_more"]/@href').extract_first()
            # 调用body_parse来获取正文内容
            yield scrapy.Request(url=body_link, meta={'aigushi_item': aigushi_item},
                                 callback=self.body_parse)
        # 获取所有的爱情小说
        for i in range(5):
            next_link = response.xpath("//div[@class='list_pages']/ul//li[11]/a/@href").extract()
            next_link = next_link[0]
            yield scrapy.Request("http://www.5aigushi.com" + next_link, callback=self.parse)

    '''
    爬取内容，这里需要多级网页爬取
    '''

    def body_parse(self, response):
        # 获取上面的数据结构
        aigushi_item = response.meta['aigushi_item']
        body_list = response.xpath('//div[@id="newstext"]//p/text()')
        body = ''
        for i_body in body_list:
            body += i_body.extract() + '\n'
        aigushi_item['story_body'] = body
        # 将数据 yield 到 pipselines中间间 中进行数据清洗啥的
        yield aigushi_item
