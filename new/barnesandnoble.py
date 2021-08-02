import os
import sys
import time
import scrapy
from scrapy.crawler import CrawlerProcess
from threading import Thread
from sys import platform
from scrapy_splash import SplashRequest
import config
import helpers

BASE_URL = "https://www.barnesandnoble.com/w/"
AFFILIATE_KEY = "barnsandnoble"

class BlogSpider4(scrapy.Spider):

    print("barsabdnoble--start---")
    searchkey = "bed"    
    goodlist = []
    timeout = 30
    start_url = 'https://www.barnesandnoble.com/s/'
    name = 'blogspider'
    
    def start_requests(self):
        yield SplashRequest(url="https://www.barnesandnoble.com/s/bed?_requestid=414948", callback=self.parse)

    def parse(self, response):
        print("response===>", response)
        obj = response.css("div.product-shelf-tile")
        print("=========obj===============", len(obj))
        if ( len(obj) == 0):
            print("barnesandnoble.com : Please Enter Correct Key.")
            return
        
        total = 0
        for li in obj:
            dic ={}
            image = li.css("div.product-image-container")
            print("image*******", image)
            if ( image is not None):
                dic['image1'] = "https:" + image.css("img::attr(src)").get()
                # dic['detail'] = helpers.format_impact_affiliate_link("https://www.barnesandnoble.com" + image.css("a::attr(href)").get(), BASE_URL,AFFILIATE_KEY)
            print("image1==>", dic['image1'])
            # print("detail-->", dic['detail'])
            price = li.css("div.current")
            if ( price is not None ):
                dic['price'] = helpers.strip_text_from_price(price.css("span::text").getall()[1])
            else: 
                dic['price']=""
            print("price==>", dic['price'])
            dic["source"] = config.sources["barnesandnoble"]
            print("source--->", dic['source'])

            total += 1

            self.goodlist.append(dic)
            if ( total >= config.max_items):
                print("barnesandnoble.com:  " , total)
                return self.goodlist     
                       
