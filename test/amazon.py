import os
import sys
import time
import scrapy
from scrapy.crawler import CrawlerProcess
from threading import Thread
import helpers
import config

BASE_URL = "https://www.amazon.com/"
AFFILIATE_KEY = "amazon"

class Amazoncom(Thread):
    def __init__(self, searchkey):
        
        if platform == "linux" or platform == "linux2":
            self.input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver")
        elif platform == "win32":
            self.input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver.exe")
        super(Amazoncom, self).__init__()
    def scroller(self, timeout):
        last_height = self.first_driver.execute_script("return document.body.scrollHeight")
        new_height = 0
        while True:
            self.first_driver.execute_script(f"window.scrollTo(0,  {new_height+100});")
            new_height +=100
            if new_height >= last_height:   break
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

class BlogSpider5(scrapy.Spider):

    searchkey = "bed"
    goodlist = []
    timeout = 30
    start_url = 'https://www.amazon.com/s?k='

    name = 'blogspider'

    def start_requests(self):
        yield scrapy.Request(url="https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=bed", callback=self.parse,headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"})

    def parse(self, response):        

        obj = response.css(".s-expand-height.s-include-content-margin")
        print("=====obj======>", len(obj))
        if ( len(obj) == 0):
            print("Amazon.com : Please Enter Correct Key.")
            return
        total = 0
        
        for li in obj:
            dic ={}
            total += 1
            print("======li======", li)
            
            image = li.css("div.s-image-square-aspect")
            if (image is not None) :
                dic['image1'] = image.css("img::attr(src)").extract()
            print("Count===>", total)
            print("=image=========>", dic['image1'])

            title = li.css("span.a-text-normal")
            if ( title is not None ):
               dic['title'] = title.css("::text").get()
            print("title====>", dic['title'])

            link = li.css("a.s-no-outline")  
            if (link is not None):
                print("href===>", link.css("a::attr(href)").extract())
                # dic["link"] = helpers.format_amazon_affiliate_link(link.css("a::attr(href)").extract())
            
            addonmessage = li.css("div.s-align-children-center")
            if (addonmessage is not None):
                dic['addonmessage'] = addonmessage.css("span::text").get()
            print("addonmessage===>", dic['addonmessage'])

            price = li.css("span.a-price")
            if (price is not None):
                dic['price'] = price.css("span::text").get()
            else:
                dic['price'] = ""
            print("price======>", dic['price'])

            rate = li.css("span.a-size-base")
            if (rate is not None):
                dic['rate'] = rate.css("span::text").get()
            print("rate===>", dic['rate'])

            dic["source"] = config.sources["amazon"]
            print("source==>", dic['source'])
            self.goodlist.append(dic)
            if ( total>=config.max_items):
                print ("amazon.com:  " , total)
                return self.goodlist

 # the script will block here until the crawling is finished