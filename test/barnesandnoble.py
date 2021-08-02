import os
import sys
import time
import scrapy
from scrapy.crawler import CrawlerProcess
from threading import Thread
import config
import helpers

BASE_URL = "https://www.barnesandnoble.com/w/"
AFFILIATE_KEY = "barnsandnoble"

class Barncom(Thread):
    def __init__(self, searchkey):       
        
        if platform == "linux" or platform == "linux2":
                self.input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver")
        elif platform == "win32":
            self.input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver.exe")
        super(Barncom, self).__init__()

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
        try:
           
            process = CrawlerProcess({
                'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
            })

            process.crawl(BlogSpider)
            process.start()
        except:
            pass

class BlogSpider4(scrapy.Spider):

    searchkey = "bed"    
    goodlist = []
    timeout = 30
    start_url = 'https://www.barnesandnoble.com/s/'
    name = 'blogspider'
    def start_requests(self):
        yield scrapy.Request(url=self.start_url + self.searchkey, callback=self.parse,headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}, meta={"proxy":"us.smartproxy.com:10000"})

    def parse(self, response):

        obj = response.css("product-shelf-tile")
        print("=========obj===============", len(obj))
        if ( len(obj) == 0):
            print("barnesandnoble.com : Please Enter Correct Key.")
            return
        
        total = 0
        for li in obj:
            dic ={}

            image = li.css("product-image-container")

            if ( image is not None):
                dic['image1'] = "https:" + image.css("::attr(src)").extract()
                image2 = image.css("::attr(href)").extract()
                dic['detail'] = helpers.format_impact_affiliate_link("https://www.barnesandnoble.com" + image2, BASE_URL,AFFILIATE_KEY)

            price = li.css("current")
            if ( price is not None ):
                dic['price'] = helpers.strip_text_from_price(price.css("a::text").get())
            else: 
                dic['price']=""

            dic["source"] = config.sources["barnesandnoble"]

            total += 1

            self.goodlist.append(dic)
            if ( total >= config.max_items):
                print("barnesandnoble.com:  " , total)
                return self.goodlist     
                       
