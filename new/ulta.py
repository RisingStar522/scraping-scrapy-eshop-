import os
import sys
import time
import scrapy
from scrapy.crawler import CrawlerProcess
from threading import Thread
from sys import platform
import config
import helpers
from scrapy_splash import SplashRequest

BASE_URL = "https://www.ulta.com/"
AFFILIATE_KEY = "ulta"
   
class BlogSpider10(scrapy.Spider):    
    name = 'blogspider10'
    goodlist = []
    timeout = 30
    start_url = 'https://www.ulta.com/ulta/a/'
    def start_requests(self):
        yield SplashRequest(url='https://www.ulta.com/ulta/a/' + self.searchkey, callback=self.parse)
    def parse(self, response):
        print("response===>", response)
        obj = response.css("div.productQvContainer")
        print(len(obj))
        if ( len(obj) == 0):
            print("ulta.com : Please Enter Correct Key.")
            return
        total = 0
        for li in obj:
            dic ={}

            image = li.css("div.quick-view-prod")

            if ( image is not None):
                dic['image1'] = image.css("a img::attr(src)").get()
                image2 = image.css("a::attr(href)").get()
                # dic['detail'] = helpers.format_impact_affiliate_link("https://www.ulta.com" + image2, BASE_URL,AFFILIATE_KEY)
            print("image1===>", dic['image1'])
            print("image2-->", image2)

            price = li.css("span.regPrice")
            if ( price is not None ):
                dic['price'] = price.css("span::text").get().replace(" ", "").replace("$", "").replace("(", "").replace("\n", "").replace("\t", "")
                # dic['price'] = helpers.strip_text_from_price(price.css("span::text").get())
            else: 
                dic['price']=""
            print("price-->", dic['price'])

            title = li.css("div.prod-title-desc")            
            if (title is not None):
                dic['title'] = title.css("a::text").get().replace(" ", "").replace("$", "").replace("(", "").replace("\n", "").replace("\t", "")
                print("title===>", dic['title'])

            rate = li.css("span.prodCellReview")
            if (rate is not None):
                dic['rate'] = rate.css("a::text").get().replace(" ", "").replace("$", "").replace("(", "").replace("\n", "").replace("\t", "")
                print("rate--->", dic['rate'])           

            shipmsg = li.css("div.product-detail-offers")   
            if ( shipmsg is not None):
                dic['shipmsg'] = shipmsg.css("p::text").get()
                print("shipmsg==>", dic['shipmsg'])
            dic["source"] = config.sources["ulta"]

            total += 1
            self.goodlist.append(dic)

            if ( total >= config.max_items):
                print("ulta.com:  " , total)
                return self.goodlist

 # the script will block here until the crawling is finished