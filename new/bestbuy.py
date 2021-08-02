import os
import sys
import time
import scrapy
from scrapy.crawler import CrawlerProcess
from threading import Thread
from sys import platform
import config
import helpers

BASE_URL = "https://www.bestbuy.com/site/"
AFFILIATE_KEY = "bestbuy"

class BlogSpider1(scrapy.Spider):

    name = 'blogspider'    
    goodlist = []
    timeout = 30
    start_url = 'https://www.bestbuy.com/site/searchpage.jsp?intl=nosplash&st='

    def start_requests(self):
        print("start")
        yield scrapy.Request(url='https://www.bestbuy.com/site/searchpage.jsp?intl=nosplash&st=/' + self.searchkey, callback=self.parse,headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"})

    def parse(self, response):

        obj = response.css(".list-item")
        print("length=========>", len(obj))
        total = 0
        if ( len(obj) == 0 ):
            print("bestbuy.com : Please Enter Correct Key.")
            return  
        for li in obj:

            dic={}

            image = li.css("a.image-link img::attr(src)").extract() 
            print("image------------><<<<", image)
            if ( image is not None ):
                dic['image1'] = image
                image2 =  li.css("a.image-link::attr(href)").extract()  
                print("image2-----<<<",image2)         
                # dic['detail'] = helpers.format_impact_affiliate_link("https://bestbuy.com/" + image2, BASE_URL, AFFILIATE_KEY)
                # print("detail-----<<<", dic['detail'])

            title = li.css("div.sku-title")
            if (title is not None):
                dic['title'] = title.css("h4 a::text").get()  
            print("title====>", dic['title'])
            rate = li.css("span.c-reviews-v4")
            if ( rate is not None ):
                dic['rate'] = rate.css("span::text").get()

            price = li.css("div.priceView-hero-price")            
            if ( price is not None ):
                price2 = price.css("span::text").get()
                print("========**************===============", price2)
                dic['price'] = helpers.strip_text_from_price(price2)
            else: 
                dic['price'] = ""
            print("price-------->", dic['price'])
            dic['source'] = config.sources['bestbuy']
            total += 1

            self.goodlist.append(dic)
            print("source----<<<<<", dic['source']) 
            if ( total >= config.max_items):
                print("bestbuy.com:  " , total)
                return self.goodlist 
                
if __name__ == '__main__':
    app.run(host= '0.0.0.0')

 # the script will block here until the crawling is finished