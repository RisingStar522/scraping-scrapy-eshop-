import os
import sys
import time
import scrapy
from scrapy.crawler import CrawlerProcess
from sys import platform
from threading import Thread
import config
import helpers

BASE_URL = "https://www.sephora.com/"
AFFILIATE_KEY = "sephora"

class Sephoracom(Thread):
    def __init__(self, searchkey): 
        
        if platform == "linux" or platform == "linux2":
            self.input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver")
        elif platform == "win32":
            self.input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver.exe")
        super(Sephoracom, self).__init__()

    def scroller(self, timeout):
        last_height = self.first_driver.execute_script("return document.body.scrollHeight")
        new_height = 0
        while True:
            self.first_driver.execute_script(f"window.scrollTo(0,  {new_height+100});")
            new_height +=50
            if new_height >= last_height*10:
                break
        time.sleep(2)

    def run(self):
        try : 
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
    start_url = 'https://www.sephora.com/search?keyword=bed'

    def start_requests(self):
        yield scrapy.Request("https://www.sephora.com/search?keyword=bed", callback=self.parse)

    def parse(self, response):

        print("response---", response.body)
        obj = response.css("a.css-ix8km1")
        print("===================",len(obj))
        
        if ( len(obj) == 0):
            print("Bedbathandbeyond.com : Please Enter Correct Key.")
            return
        total = 0
        for li in obj:
            dic ={}

            image = li.css("div.css-z3rgf2 div.css-1gp6ra2 picture.css-yq9732 img::attr(src)").extract()
            print("image==>", image)
            if ( image is not None):
                dic['image1'] = "https://www.sephora.com/" + image
                image2 = li.css("a.css-ix8km1::attr(href)").extract()
                print("image2==>", image2)
                dic['detail'] = helpers.format_impact_affiliate_link("https://www.bedbathandbeyond.com" + image2, BASE_URL,AFFILIATE_KEY)
            print("detail==>", dic['detail'])

            price = li.css("span.sku_item_price_list")
            if ( price is not None ):
                pass
                dic['price'] = helpers.strip_text_from_price(price.css("span::text").get())
            else: 
                dic['price']=""
            print("price==>", dic['price'])

            title = li.css("div.css-1gughuu")            
            if (title is not None):
                dic['title'] = title.css("spsn::text").get()
            print("title==>", dic['title'])

            rate = li.css("div.css-t33ub8")
            if (rate is not None):
                dic['rate'] = rate.css("span::text").get()
            print("rate==>", dic['rate'])

            dic["source"] = config.sources["sephora"]

            total += 1
            self.goodlist.append(dic)

            if ( total >= config.max_items):
                print("sephora.com:  " , total)
                return self.goodlist  
            
                
 # the script will block here until the crawling is finished