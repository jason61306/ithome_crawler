# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IthomeItem(scrapy.Item):
    Tags = scrapy.Field()
    Url = scrapy.Field()
    Title = scrapy.Field()
    Author = scrapy.Field()
    Publish_Date = scrapy.Field()
    Picture = scrapy.Field()
    Picture_Title = scrapy.Field()
    Content = scrapy.Field()
    Facebook = scrapy.Field()
    Log = scrapy.Field()

class FacebookItem(scrapy.Item):
    Like = scrapy.Field()
    Message = scrapy.Field()
    Update_Time = scrapy.Field()

class LogItem(scrapy.Item):
    Id = scrapy.Field()
    Crawled_Time = scrapy.Field()


