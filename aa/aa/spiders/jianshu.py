# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from items import JianshuItem
from urllib.parse import urljoin
import re
from scrapy.loader import ItemLoader
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
count=0

class JianshuSpider(scrapy.Spider):
    name = 'jianshu'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/c/5AUzod']


    def __init__(self):
        self.broswer = webdriver.Chrome(executable_path=r'D:\57635\chromedriver.exe')

        super().__init__()
        dispatcher.connect(self.spider_closed,signals.spider_closed)#信号量

    def spider_closed(self,spider):
        print("完成")
        self.broswer.quit()#退出


    def parse(self, response):
        for i in range(1,500):
            url='https://www.jianshu.com/c/5AUzod?order_by=added_at&page='+str(i)
            pageurlist=response.xpath('//*[@id="list-container"]/ul/li')
            for i in pageurlist:
                x=i.xpath('//div[@class="content"]/a')
                pageurl=urljoin(base="https://www.jianshu.com",url=x.attrib["href"])
                imageurl=i.css('a[class="wrap-img"] > img::attr(src)').extract_first()

                yield Request(url=pageurl,meta={'imageurl':imageurl},callback=self.parse_item)

            yield Request(url=url,callback=self.parse,dont_filter=False)

    def parse_item(self,response):
        item=ItemLoader(item=JianshuItem(),response=response)
        item.add_xpath('title','/html/body/div[1]/div[2]/div[1]/h1/text()')
        item.add_value('likes',re.findall('<script type="application/json" data-name="page-data">(.*?)</script>',response.body.decode('utf-8')))
        item.add_css('author','body > div.note > div.post > div.article > div.author > div > span > a::text')
        item.add_value('noteid',response.url)
        item.add_value('imageurl',response.meta['imageurl'])

        yield item.load_item()
