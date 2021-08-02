import os
import sys
import time
import scrapy
from scrapy.crawler import CrawlerProcess
from threading import Thread
from scrapy_splash import SplashRequest
from sys import platform
import config
import helpers

BASE_URL = "https://www.bedbathandbeyond.com/store/product/"
AFFILIATE_KEY = "bedbat"

        
class BlogSpider(scrapy.Spider):

    name = 'blogspider'
    print("name ===>", name)
    goodlist = []
    def start_requests(self):
        print("start_request", self.searchkey)
        yield SplashRequest(url='https://www.bedbathandbeyond.com/store/s/' + self.searchkey, callback=self.parse)
   
    def parse(self, response):

        obj = response.css("article.tealium-product-card")
        print("======obj=======", len(obj))
        if ( len(obj) == 0):
            print("Bedbathandbeyond.com : Please Enter Correct Key.")
            return
        
        total = 0
        for li in obj:
            dic ={}           

            image = li.css("div.Thumbnail_4q2qnF img::attr(src)").extract()

            if ( image is not None):
                dic['image1'] = image
                print("image1===>", dic['image1'])
                image2 = li.css("div.ProductTile-inline_6bSQ4q a::attr(href)").extract()
                print("image2----->", image2)
                #dic['detail'] = helpers.format_impact_affiliate_link("https://www.bedbathandbeyond.com" + image2, BASE_URL, AFFILIATE_KEY)
                
            price = li.css("span.Price_3HnIBb")
            if ( price is not None ):
                pass
                dic['price'] = helpers.strip_text_from_price(price.css("span::text").get())
            else: 
                dic['price']=""

            print("price===>", dic['price'])

            title = li.css("div.tealium-product-title")            
            if (title is not None):
                dic['title'] = title.css("a::text").get()
            
            rate = li.css("span.Rating_3RTQ2U")
            if (rate is not None):
                dic['rate'] = rate.css("span::text").get()            

            shipmsg = li.css("p.ProductTile-inline_36NSEc")   
            if ( shipmsg is not None):
                dic['shipmsg'] = shipmsg.css("p::text").get()

            dic["source"] = config.sources["bedbathandbeyond"]
            print("source=====>", dic['source'])
            total += 1

            self.goodlist.append(dic)
            if ( total >= config.max_items):
                print("bedbat.com:  " , total)
                return self.goodlist
 # the script will block here until the crawling is finished