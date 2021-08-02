import scrapy
from scrapy.crawler import CrawlerProcess
import config
import helpers
from threading import Thread

BASE_URL = "https://www.ulta.com/"
AFFILIATE_KEY = "ulta"

class Ultacom(Thread):
    def __init__(self, searchkey):
        self.searchkey = searchkey
        # self.first_driver = first_driver
        self.goodlist = []
        self.timeout = 30
    
        self.start_url = 'https://www.ulta.com/'
        
        if platform == "linux" or platform == "linux2":
                self.input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver")
        elif platform == "win32":
                self.input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver.exe")
        super(Ultacom, self).__init__()
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
            self.first_driver = self.open_chrome()
            self.first_driver.delete_all_cookies()
            chrome = self.first_driver.get(self.start_url)

            searh_input = self.first_driver.find_element_by_xpath('//input[@id="searchInput"]')
            searh_input.clear()
            searh_input.send_keys(self.searchkey)
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
        yield scrapy.Request(url=self.start_url + self.searchkey, callback=self.parse,headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}, meta={"proxy":"us.smartproxy.com:10000"})

    def parse(self, response):

        obj = response.css("productQvContainer")
        # print(obj)
        if ( len(obj) == 0):
            print("ulta.com : Please Enter Correct Key.")
            return
        total = 0
        for li in obj:
            dic ={}

            image = li.css("a.product img::attr(src)").extract()

            if ( image is not None):
                dic['image1'] = image
                image2 = li.css("div.ProductTile-inline_6bSQ4q a::attr(href)").extract()
                dic['detail'] = helpers.format_impact_affiliate_link("https://www.ulta.com" + image2, BASE_URL,AFFILIATE_KEY)

            price = li.css("span.regPrice")
            if ( price is not None ):
                pass
                dic['price'] = helpers.strip_text_from_price(price.css("span::text").get())
            else: 
                dic['price']=""

            title = li.css("a.prod-title-desc")            
            if (title is not None):
                dic['title'] = title.css("a::text").get()
            
            rate = li.css("span.prodCellReview")
            if (rate is not None):
                dic['rate'] = rate.css("span::text").get()            

            shipmsg = li.css("p.product-detail-offers")   
            if ( shipmsg is not None):
                dic['shipmsg'] = shipmsg.css("p::text").get()

            dic["source"] = config.sources["ulta"]

            total += 1
            self.goodlist.append(dic)

            if ( total >= config.max_items):
                print("barnesandnoble.com:  " , total)
                self.first_driver.quit()
                return   

 # the script will block here until the crawling is finished