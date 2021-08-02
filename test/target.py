import scrapy
from scrapy.crawler import CrawlerProcess
import config
import helpers
from threading import Thread

BASE_URL = "https://www.target.com/s/"
AFFILIATE_KEY = "target"


class Targetcom(Thread):

    def __init__(self, searchkey):
        print("HERER")
        print(searchkey)
        self.searchkey = searchkey
        # self.first_driver = first_driver
        self.goodlist = []
        self.timeout = 30
        self.start_url = "https://www.target.com/s?searchTerm="
        
        if platform == "linux" or platform == "linux2":
                self.input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver")
        elif platform == "win32":
                self.input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver.exe")
        else:
            self.input_dir =  "/usr/local/bin/chromedriver"

        super(Targetcom, self).__init__()

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
            
class BlogSpider(scrapy.Spider):

    name = 'blogspider'
    searchkey = "bed"
    goodlist = []
    timeout = 30
    start_url = "https://www.target.com/s?searchTerm=bed"

    def start_requests(self):
        yield scrapy.Request(url=self.start_url + self.searchkey, callback=self.parse,headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}, meta={"proxy":"us.smartproxy.com:10000"})

    def parse(self, response):

        print("****************", response.body)
        obj = response.css("li.h-padding-a-none")
        print("===============", obj)
        if ( len(obj) == 0):
            print("Target.com : Please Enter Correct Key.")
            return
        total = 0
        for li in obj:

            dic ={}
            detail2 = li.css("a::attr(href)").extract()
            dic['detail'] = helpers.format_impact_affiliate_link("https://www.target.com/" + detail2, BASE_URL, AFFILIATE_KEY)
                     
            pic = li.css("picture")
            if ( len(pic) ==1 ):
                dic['image1'] = li.css("picture source::attr(srcset)").extract()
            if ( len(pic)==2):
                dic['image1'] = li.css("picture source::attr(srcset)")[0].extract()
                dic['image2'] = li.css("picture source::attr(srcset)")[1].extract()
  
            title = li.css("a.Link-sc-1khjl8b-0 styles__StyledTitleLink-mkgs8k-5")            
            if (title is not None):
                dic['title'] = title.css("a::text").get()
            
            catjack = li.cww("div.BrandAndRibbonMessage__BrandAndRibbonWrapper-z07dc0-0")
            if catjack is not None : 
                dic['catjack'] = catjack.css("a::text").get()

            newat = li.css("div.BrandAndRibbonMessage__BrandAndRibbonWrapper-z07dc0-0")
            if newat is not None : 
                dic['newat'] = newat.css("a::text").get()

            rate = li.css("span.RatingStarBlock__RatingCountText-sc-1pjp5ox-0")
            if rate is not None : 
                dic['rate'] = rate.css("span::text").get()
            
            price  = li.css("div.styles__StyledPricePromoWrapper-mkgs8k-9")
            if price is not None : 
                dic['price'] = helpers.strip_text_from_price(price.css("span::text").get())
            else: 
                dic['price']=''

            addon = li.css("div.h-margin-t-tiny h-text-grayDark" )
            if addon is not None : 
                dic['addonmessage'] = addon.css("::text").get()           

            shipmsg = li.css("span.LPFulfillmentSectionShippingFA_shippingMessage")   
            if ( shipmsg is not None):
                dic['shipmsg'] = shipmsg.css("span::text").get()

            shipobj = li.css("span.LPFulfillmentSectionShippingFA_standardShippingMessage")
            if shipobj is not None : 
                dic['shipping'] =  shipobj.css("span::text").get() + shipobj.css("::text").get()

            stomsg = li.css("div.LPFulfillmentSectionStoreFA_storeMessaging")
            if stomsg is not None :
                nearby = li.css("div.LPFulfillmentSectionStoreFA_checkNearbyStores")
                if ( nearby is not None):
                    dic['boston'] = stomsg.css("div div::text").get()
                else:
                    dic['limit'] = stomsg.css("div a::text").get() + stomsg.css("div::text").get()
                
                outmsg = li.find("div", attrs={"data-test": "LPFulfillmentSectionStoreFA_OPUMessaging"})
                if outmsg is not None : dic['limit'] = outmsg.span.get_text() + outmsg.get_text()

                dic["source"] = config.sources["target"]

                self.goodlist.append(dic)
                total+=1

                if ( total>=config.max_items):
                    print("target.com   ",  total)
                    self.first_driver.quit()
                    return self.goodlist
 # the script will block here until the crawling is finished