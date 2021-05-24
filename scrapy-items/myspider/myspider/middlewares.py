# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import json


class MyUserAnger(object,):

    def process_request(self, request, spider):

        agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66'
        # agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'

        referer='https://careers.tencent.com/search.html'

        request.headers['user-agent'] = agent
        request.headers['referer'] = referer

        # request.headers[':authority'] = authority
        # request.headers[':path'] = path
        # request.headers['origin'] = origin
        # request.headers['content-type'] = contentype
        # print(request.headers['cookie'])
