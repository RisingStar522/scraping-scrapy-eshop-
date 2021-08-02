import os
import sys
import time
import scrapy
from scrapy.crawler import CrawlerProcess
from threading import Thread
from sys import platform
import config
import helpers

BASE_URL = "https://www.sears.com/"
AFFILIATE_KEY = "sears"

class Searscom(Thread):
    def __init__(self, searchkey):
        self.searchkey = searchkey
        # self.first_driver = first_driver
        self.goodlist = []
        self.timeout = 30
        self.start_url = 'https://www.sears.com/search=bed'
        
        if platform == "linux" or platform == "linux2":
            self.input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver")
        elif platform == "win32":
            self.input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver.exe")
        super(Searscom, self).__init__()

    def scroller(self, timeout):
        last_height = self.first_driver.execute_script("return document.body.scrollHeight")
        new_height = 0
        while True:
            self.first_driver.execute_script(f"window.scrollTo(0,  {new_height+100});")
            new_height +=100
            if new_height >= last_height*10:
                break
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
class BlogSpider(scrapy.Spider):

    name = 'blogspider'
    searchkey = "bed"    
    goodlist = [] 
    start_url = 'https://www.sears.com/search=bed'

    def start_requests(self):
        yield scrapy.Request(url = "https://www.sears.com/search=bed", callback=self.parse,headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"})

    def parse(self, response):

        print("response===<<<<" ,response)
        obj = response.css("div.card-container").getall()
        print("==============", len(obj))
        if ( len(obj) == 0):
            print("sears.com : Please Enter Correct Key.")
            return
        total = 0
        for li in obj:
            dic ={}

            image = li.css("a.card-image-height-content img::attr(src)").extract()
            print("image---->", image)
            if ( image is not None):
                dic['image1'] = image
                image2 = li.css("a::attr(href)").extract()
                print("image2----->", image2)
                # dic['detail'] = helpers.format_impact_affiliate_link("https://www.sears.com" + image2, BASE_URL,AFFILIATE_KEY)

            price = li.css("span.card-price-orig")
            if ( price is not None ):
                pass
                dic['price'] = helpers.strip_text_from_price(price.css("span::text").get())
            else: 
                dic['price']=""
            print("price====>", dic['price'])
            title = li.css("h3.card-title")            
            if (title is not None):
                dic['title'] = title.css("a::text").get()
            
            rate = li.css("span.!!product.reviewCount")
            if (rate is not None):
                dic['rate'] = rate.css("span::text").get()            

            shipmsg = li.css("span.product.storeOrigin")   
            if ( shipmsg is not None):
                dic['shipmsg'] = shipmsg.css("span::text").get()
            print("shipmsg==>", shipmsg)

            shipping = li.css("span.product.bestDealMessage")
            if ( shipping is not None ):
                dic['shipping'] = shipping.css("span::text").get()
            print("shipping==", dic['shipping'])

            dic["source"] = config.sources["bedbathandbeyond"]
            print("source----", dic['source'])

            total += 1
            self.goodlist.append(dic)

            if ( total >= config.max_items):
                print("barnesandnoble.com:  " , total)
                return self.goodlist
 # the script will block here until the crawling is finished