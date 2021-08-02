
import os
import sys
import time
import scrapy
from scrapy.crawler import CrawlerProcess
from threading import Thread
from sys import platform
import config
import helpers

BASE_URL = "https://www.newegg.com/"
AFFILIATE_KEY = "newegg"

class Neweggcom(Thread):
    def __init__(self, searchkey):
        self.searchkey = searchkey
        # self.first_driver = first_driver
        self.goodlist = []
        self.timeout = 30
        self.start_url = 'https://www.newegg.com/p/pl?d='
        if platform == "linux" or platform == "linux2":
            self.input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver")
        elif platform == "win32":
            self.input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver.exe")
        super(Neweggcom, self).__init__()
                
    def scroller(self, timeout):
        last_height = self.first_driver.execute_script("return document.body.scrollHeight")
        new_height = 0
        while True:
            self.first_driver.execute_script(f"window.scrollTo(0,  {new_height+100});")
            new_height +=100
            if new_height >= last_height:   break
        time.sleep(1)

    def run(self):
        try : 
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
            
class BlogSpider2(scrapy.Spider):

    name = 'blogspider'
    searchkey = "bed"
    goodlist = []
    start_url = 'https://www.newegg.com/p/pl?d='

    def start_requests(self):
        yield scrapy.Request(url="https://www.newegg.com/p/pl?d=/bed", callback=self.parse,headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"})

    def parse(self, response):

        obj = response.css("div.item-cell")
        
        if ( len(obj) == 0):
            print("newegg.com : Please Enter Correct Key.")
            return

        total = 0

        for li in obj:
            dic ={}

            image = li.css("div.item-container")            
            if ( image is not None):
                dic['image1'] = image.css("a.item-img img::attr(src)").extract()
                print("image1====>", dic['image1'])
                image2 = image.css("a.item-img::attr(href)").extract()
                print("image2---->", image2)
                dic['detail'] = image2

            rate = li.css("span.item-rating-num")
            if (rate is not None):
                dic['rate'] = rate.css("span::text").get()
            print("rate---->", dic['rate'])

            title = li.css("a.item-title::text").get() 
            print("title===>>>>>", title)          
            if (title is not None):
                dic['title'] = title

            price = li.css("li.price-current")
            print("price*******", price)
            if ( price is not None ): 
                if (price.css("li::text").get() is not None):                    
                    dic['price'] = helpers.strip_text_from_price(price.css("li::text").get()+price.css("strong::text").get()+price.css("sup::text").get())
                else:
                    dic['price']=""
            else: 
                dic['price']=""
            print("price====>", dic['price'])

            shipmsg = li.css("li.price-ship")   
            if ( shipmsg is not None):
                dic['shipmsg'] = shipmsg.css("li::text").get()

            dic["source"] = config.sources["newegg"]
            print("source---->", dic['source'])
            total += 1
            self.goodlist.append(dic)

            if ( total >= config.max_items):
                print("newegg.com:  " , total)
                return self.goodlist   

 # the script will block here until the crawling is finished