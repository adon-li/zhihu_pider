# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
class ZhihutestPipeline(object):
        def __init__(self):
            self.f = open('user.json', 'wb')

        def process_item(self, item, spider):
            # print(dict(item))
            # print(type(dict(item)))
            content = json.dumps(dict(item),ensure_ascii=False) + ",\n"
            # print(content)
            # print(type(content))
            self.f.write(content.encode("utf-8"))
            return item

        def close_spider(self, spider):
            self.f.close()
