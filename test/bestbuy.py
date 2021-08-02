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

class Bestbuycom(Thread):    
    def __init__(self, searchkey):      
       
        if platform == "linux" or platform == "linux2":
            self.input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver")
        elif platform == "win32":
            self.input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver.exe")

        super(Bestbuycom, self).__init__()

    def scroller(self, timeout):
        print("scroller=====>")
        last_height = self.first_driver.execute_script("return document.body.scrollHeight")
        new_height = 0
        while True:
            self.first_driver.execute_script(f"window.scrollTo(0,  {new_height+100});")
            new_height +=100
            if new_height >= last_height:   break
        time.sleep(1)


    def run(self):
        try:
            print("try-----except---->")
            # self.first_driver = self.open_chrome()
            # self.first_driver.delete_all_cookies()
            # chrome = self.first_driver.get(self.start_url + self.searchkey)
            process = CrawlerProcess({
                'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
            })

            process.crawl(BlogSpider)
            process.start()
        except:
            pass

class BlogSpider1(scrapy.Spider):

    name = 'blogspider'
    searchkey = 'bed'
    goodlist = []
    timeout = 30
    start_url = 'https://www.bestbuy.com/site/searchpage.jsp?intl=nosplash&st='

    def start_requests(self):
        print("start")
        yield scrapy.Request(url='https://www.bestbuy.com/site/searchpage.jsp?intl=nosplash&st=/bed', callback=self.parse,headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"})

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

 # the script will block here until the crawling is finished