# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class TengxunPipeline(object):
    def __init__(self):
        self.file = open('tengxunjob.json', 'w', encoding='utf-8')

    def process_item(self, items, spider):
        items = dict(items)
        str_data = json.dumps(items, ensure_ascii=False,) + ',\n'
        self.file.write(str_data)

        return items

    def __del__(self):
        self.file.close()
