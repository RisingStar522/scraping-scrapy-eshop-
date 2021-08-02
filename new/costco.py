import os
import sys
import time
import scrapy
from scrapy.crawler import CrawlerProcess
from threading import Thread
import config
import helpers

BASE_URL = "https://www.costco.com/"
AFFILIATE_KEY = "costco"     
 

class BlogSpider11(scrapy.Spider):

    goodlist = []
    timeout = 30
    start_url = "https://www.costco.com/CatalogSearch?dept=All&keyword="        

    name = 'blogspider11'
    print("costco.com===start")
    def start_requests(self):
        yield scrapy.Request(url="https://www.costco.com/CatalogSearch?dept=All&keyword=" + self.searchkey, callback=self.parse,headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"})


    def parse(self, response):

        obj = response.css("div.thumbnail")
        print("=========obj===============", len(obj))

        if ( len(obj) == 0):
            print("costco.com : Please Enter Correct Key.")
            return
        
        total = 0
        for li in obj:
            dic ={}
            print("for--start")
            image = li.css("img.img-responsive::attr(src)").extract()
            print("image====<<<",image)

            if ( image is not None):
                dic['image1'] = image
            elif(li.css("data-src::attr(src)").extract()):
                dic['imgae1'] = li.css("data-src::attr(src)").extract()

            price = li.css("div.price")
            if ( price is not None ):
                dic['price'] = helpers.strip_text_from_price(price.css("::text").get())
            else: 
                dic['price']=""
            print("price=====>", dic['price'])

            title = li.css("span.description") 
            if (title is not None):
                dic['title'] = title.css("a::text").get()
                # dic['detail'] = helpers.format_impact_affiliate_link(title.css("a::href()").extract())
            print("title-->", dic['title'])           
            
            rate = li.css("div.ratings-number")            
            if (rate is not None):
                dic['rate'] = rate.css("div::text").get().replace("\t", "").replace("\n", "").replace(" ","")
            print("rate--=-=-=-><><", dic['rate'])
            shipmsg = li.css("p.promo")   
            if ( shipmsg is not None):
                dic['shipmsg'] = shipmsg.css("p::text").get()
            print("shipmsg==>", dic['shipmsg'])
            dic["source"] = config.sources["costco"]
            print("source--->", dic['source'])
            total += 1
            self.goodlist.append(dic)

            if ( total >= config.max_items):
                print("costco.com:  " , total)
                return self.goodlist 


 # the script will block here until the crawling is finished