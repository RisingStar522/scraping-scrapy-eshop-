import os
import sys
import time
import scrapy
from scrapy.crawler import CrawlerProcess
import config
import helpers
from threading import Thread

BASE_URL = "https://www.walmart.com/"
AFFILIATE_KEY = "walmart"

class Walmartcom(Thread):
    def __init__(self, searchkey):

        self.start_url = 'https://www.walmart.com/search/?query='

        if platform == "linux" or platform == "linux2":
            self.input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver")
        elif platform == "win32":
            self.input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver.exe")
        super(Walmartcom, self).__init__()

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
class BlogSpider3(scrapy.Spider):

    searchkey = "bed"
    goodlist = []
    timeout = 30
    start_url = 'https://www.walmart.com/search/?query='

    name = 'blogspider'
    def start_requests(self):
        yield scrapy.Request(url="https://www.walmart.com/search/?query=bed", callback=self.parse,headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"})

    def parse(self, response):

        obj = response.css("div.search-result-gridview-item")
        print("obj===>", len(obj)) 

        if ( len(obj) == 0):
            print("Walmart.com : Please Enter Correct Key.")
            return

        total = 0

        for li in obj:
            dic ={}

            detail = li.css("a.search-result-productimage")            
            if (detail is not None):
                detail2 = detail.css("a::attr(href)").extract()
                print("detail2----->", detail2)
                # dic['detail'] = helpers.format_impact_affiliate_link('https://www.walmart.com/' + detail2, BASE_URL, AFFILIATE_KEY)

            title = li.css("a.product-title-link")            
            if (title is not None):
                dic['title'] = title.css("span::text").get()
            print("title---->", dic['title'])

            rate = li.css("span.stars-reviews-count")
            if (rate is not None):
               dic['rate'] = rate.css("span::text").get()            
            print("rate---->", dic['rate'])

            price = li.css("span.price-main")
            if ( price is not None ): 
                price2 = price.css("span::text").get()               
                dic['price'] = helpers.strip_text_from_price(price2)
            else: 
                dic['price']=""
            print("price--->", dic['price'])

            dic["source"] = config.sources["walmart"]  
            print("source--->", dic['source'])

            shipdetail = li.css("div.search-result-product-shipping-details")   
            if ( shipdetail is not None):
                dic['ship'] = shipdetail.css("span::text").get()
            print("shipdetail--->", dic['ship'])
            
            total += 1
            self.goodlist.append(dic)

            if ( total >= config.max_items):
                print("walmart.com:  " , total)
                return  self.goodlist 
 # the script will block here until the crawling is finished