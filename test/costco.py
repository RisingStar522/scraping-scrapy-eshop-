import scrapy
from scrapy.crawler import CrawlerProcess
from threading import Thread
import config
import helpers

BASE_URL = "https://www.costco.com/"
AFFILIATE_KEY = "Costco"

class Costcocom(Thread):
    def __init__(self, searchkey):
        self.searchkey = searchkey
        # self.first_driver = first_driver
        self.goodlist = []
        self.timeout = 30
        self.start_url = 'https://www.bestbuy.com/site/searchpage.jsp?intl=nosplash&st='

        if platform == "linux" or platform == "linux2":
            self.input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver")
        elif platform == "win32":
            self.input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver.exe")

        super(Bestbuycom, self).__init__()

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
            self.first_driver = self.open_chrome()
            self.first_driver.delete_all_cookies()
            chrome = self.first_driver.get(self.start_url + self.searchkey)
            process = CrawlerProcess({
                'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
            })

            process.crawl(BlogSpider)
            process.start()
        except:
            pass
class BlogSpider(scrapy.Spider):

    name = 'blogspider'
    def start_requests(self):
        yield scrapy.Request(url=self.start_url + self.searchkey, callback=self.parse,headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"})


    def parse(self, response):

        obj = response.css("div.thumbnail")
        print("=========obj===============", len(obj))

        if ( len(obj) == 0):
            print("costco.com : Please Enter Correct Key.")
            return
        
        total = 0
        for li in obj:
            dic ={}

            image = li.css("img::attr(src)").extract()

            if ( image is not None):
                dic['image1'] = image
            elif(li.css("data-src::attr(src)").extract()):
                dic['imgae1'] = li.css("data-src::attr(src)").extract()

            price = li.css("div.price")
            if ( price is not None ):
                dic['price'] = helpers.strip_text_from_price(price.css("::text").get())
            else: 
                dic['price']=""

            title = li.css("p.description")            
            if (title is not None):
                dic['title'] = title.css("a::text").get()
                dic['detail'] = helpers.format_impact_affiliate_link(title.css("a::href()").extract())
            
            rate = li.css("div.ratings-number")
            if (rate is not None):
                dic['rate'] = rate.css("::text").get().replace()("\t", "").replace("\n", "").replace(" ","")            

            shipmsg = li.css("p.promo")   
            if ( shipmsg is not None):
                dic['shipmsg'] = shipmsg.css("p::text").get()

            dic["source"] = config.sources["costco"]

            total += 1
            self.goodlist.append(dic)

            if ( total >= config.max_items):
                print("costco.com:  " , total)
                self.first_driver.quit()
                return      


 # the script will block here until the crawling is finished