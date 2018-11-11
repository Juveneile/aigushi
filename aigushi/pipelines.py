# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class AigushiPipeline(object):
    # 打开文件
    def open_spider(self, spider):
        self.f = open('story.txt', 'a', encoding='utf-8')

    # 关闭文件
    def close_spider(self, spider):
        self.f.close()

    # 保存
    def process_item(self, item, spider):
        # 字典类的转换成字符串 ensure_ascii 中文编码
        story = dict(item)
        self.f.write(story['story_name'] + '\n\n')
        self.f.write(story['story_body'] + '\n\n\n')
        return item
