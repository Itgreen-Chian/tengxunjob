# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 职位名称
    PostName = scrapy.Field()
    # 职位详情连接
    PostURL = scrapy.Field()
    # 职位类别
    CategoryType = scrapy.Field()
    # 工作地点
    LocationName = scrapy.Field()
    # 最新发布时间
    LastUpdateTime = scrapy.Field()
    # 工作职责
    Requirement = scrapy.Field()
    # 工作要求
    Responsibility = scrapy.Field()



