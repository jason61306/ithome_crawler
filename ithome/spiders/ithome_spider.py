# !/usr/bin/python
# coding:utf-8
import scrapy
import sys
import time
import json

from ithome.items import IthomeItem, FacebookItem, LogItem

SOURCE = 'ithome'
ITHOME = 'https://www.ithome.com.tw'

class ithomeSpider(scrapy.Spider):
    name = 'ithome'

    def __init__(self, env='development', start=1, end=sys.maxint):
        self.start = int(start)
        self.end = int(end)
        self.env = env
        #171218.K.Y.:利用以下網址導到文章列表最後一頁,已取得總頁數
        self.start_urls =  [ ITHOME + '/security?page=999999999999999']

    def parse(self, response):
        page_num = int(response.xpath('//li[@class="active last"]//a/text()').extract()[0])
        if page_num > self.end:
            page_num = self.end

        for page in xrange(self.start - 1, page_num):
            url = ITHOME + '/security?page=' + str(page)
            yield scrapy.Request(url, callback=self.parse_ithome_list)
    
    def parse_ithome_list(self, response):
        parse_list = response.xpath('//div[@class="view-content"]')[3].xpath('div')
        for data in parse_list:
            #171219.K.Y.:從文章列表取得文章url及tag
            ithome = IthomeItem()
            log = LogItem()
            url = str(data.xpath('div[@class="item"]/p[@class="photo"]/a/@href').extract()[0])
            log['Id'] = filter(str.isdigit, url)
            log['Crawled_Time'] = int(time.time())
            ithome['Log'] = log
            ithome['Url'] = ITHOME + url
            tags = []
            for tag in data.xpath('div[@class="item"]/p[@class="category"]/a/text()').extract():
                tags.append(tag.encode('utf-8'))
            ithome['Tags'] = tags
            yield scrapy.Request(ithome['Url'], callback=self.parse_article, meta={'ithome':ithome})

    def parse_article(self, response):
        #171219.K.Y.:取得文章詳細內容,Picture_Title可能沒有,用try,except避免錯誤
        ithome = response.meta['ithome']
        ithome['Title'] = response.xpath('//h1[@class="page-header"]/text()').extract()[0].encode('utf-8')
        ithome['Author'] = response.xpath('//span[@class="author"]/a/text()').extract()[0].encode('utf-8')
        ithome['Publish_Date'] = response.xpath('//span[@class="created"]/text()').extract()[0].encode('utf-8')
        ithome['Picture'] =response.xpath('//div[@class="img-wrapper"]//img/@src').extract()[0].encode('utf-8')
        try:
            ithome['Picture_Title'] = response.xpath('//p[@class="caption"]/text()').extract()[0].encode('utf-8')
        except:
            ithome['Picture_Title'] = ''
        content=''
        content_list = response.xpath('//div[@class="field field-name-body field-type-text-with-summary field-label-hidden"]//text()').extract()
        for content_fragment in content_list:
            content = content + content_fragment
        ithome['Content'] = content.encode('utf-8')
        #171219.K.Y.:取得facebook按讚及留言
        facebook_api_like_url = 'https://graph.facebook.com/?id={}'.format(ithome['Url'])
        yield scrapy.Request(facebook_api_like_url, callback=self.parse_fb, meta={'ithome':ithome})

    def parse_fb(self, response):
        ithome = response.meta['ithome']
        fb_detail = json.loads((response.body))
        facebook = FacebookItem()
        facebook['Like'] = fb_detail['share']['share_count']
        facebook['Message'] = fb_detail['share']['comment_count']
        facebook['Update_Time'] = fb_detail['og_object']['updated_time']
        ithome['Facebook'] = facebook
        yield ithome
