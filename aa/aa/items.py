# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose,TakeFirst

class AaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def callme(value):
    print("我被调用啦")
    # temp=value['likes'][0].replace("\'", '\"')
    # print(temp)
    # value['likes'] = temp['note']['likes_count']
    return value

class JianshuItem(scrapy.Item):

    title=scrapy.Field()
    likes=scrapy.Field(
        output_processor=MapCompose(callme))#把这个里面的东西出来
    author=scrapy.Field()
    imageurl=scrapy.Field(
        input_processor=MapCompose(lambda x: "http:"+x.split("?")[0])
    )
    noteid=scrapy.Field()