import os
import sys
import time
from threading import Thread
from sys import platform
from bs4 import BeautifulSoup
from lxml import html
from selenium import webdriver

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import config
import helpers

BASE_URL = "https://www.target.com/p/"
AFFILIATE_KEY = "target"

class Targetcom(Thread):

    def __init__(self, searchkey):
        print("HERER")
        print(searchkey)
        self.searchkey = searchkey
        self.first_driver = ''
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
        print('sadfasdf')
        try:
            self.first_driver = self.open_chrome()            
            self.first_driver.delete_all_cookies()
            chrome = self.first_driver.get(self.start_url + self.searchkey)
            # if (chrome is None):
            #     self.first_driver.quit()
            #     print( "target.com : Access Denied")
            #     return 
            time.sleep(1)       
            
            total = 0
            

            while True:
                self.scroller(2)
                # driver = self.first_driver
                # eles = driver.find_elements_by_class_name('h-padding-a-none')
                # for ele in eles:
                #     print("======")
                soup = BeautifulSoup( self.first_driver.page_source, "html.parser")
                obj = soup.find_all("li", class_="h-padding-a-none")
                time.sleep(1)
                if ( len(obj)==0):
                    print( "Target.com: Please Enter Coreect Key.")
                    self.first_driver.quit()
                    return []
            
                try:
                    for li in obj:
                        dic ={}
                        # dic['detail'] = helpers.format_impact_affiliate_link("https://www.target.com/" + li.a['href'], BASE_URL, AFFILIATE_KEY)
                        print("start1---") 
                        pic =  li.find_all("picture")
                        print("start1====", len(pic)) 
                       
                        print("start1")                         
                        if ( len(pic)>=2):                         
                            dic['image1'] = li.picture.source['srcset']
                            dic['image2'] = li.picture.next_sibling.source['srcset']
                        elif():
                            dic['image2'] = ""
                            dic['image1'] = li.picture.source['srcset']
                            
                        print("image1=====>", dic['image1'])
                        print("image2=====>", dic['image2'])
                        title = li.find(class_="styles__StyledTitleLink-mkgs8k-5")
                        if title is not None : dic['title'] = title.get_text()
                        print("title--->", dic['title'])
                        
                        catjack = li.find(class_="BrandAndRibbonMessage__BrandAndRibbonWrapper-z07dc0-0")
                        if catjack is not None : 
                            dic['catjack'] = catjack.a.get_text() 
                        else: 
                            dic['catjack'] = ""
                        print("catjack---->", dic['catjack'])
                        # newat = li.find(class_="BrandAndRibbonMessage__BrandAndRibbonWrapper-z07dc0-0 gBsyfJ")
                        # if newat is not None : dic['newat'] = newat.a.get_text()
                        # print("newat==>", dic['newat'])
                        rate = li.find(class_ = "RatingStarBlock__RatingCountText-sc-1pjp5ox-0")
                        if rate is not None : dic['rate'] = rate.get_text()
                        print("rate--->", dic['rate'])
                        price  = li.find(class_="styles__StyledPricePromoWrapper-mkgs8k-9")
                        if price is not None : dic['price'] = price.span.get_text()
                        else: dic['price']=''
                        print("price==>", dic['price'])
                        addon = li.find(class_="h-text-grayDark" )
                        if addon is not None : 
                            dic['addonmessage'] = addon.get_text()
                        else:
                            dic['addonmessage'] = ""
                        print("addonmessage==>", dic['addonmessage'])
                        shipmsg = li.find(class_="h-text-greenDark")
                        print("shipmsg-->", shipmsg)
                        if shipmsg is not None : 
                            dic['shipmsg'] = shipmsg.get_text()
                        else:
                            dic['shipmsg'] = ""
                        print("shipmsg==>", dic['shipmsg'])
                        # shipobj = li.find('span', attrs={'data-test': "LPFulfillmentSectionShippingFA_standardShippingMessage"})
                        # if shipobj is not None : dic['shipping'] =  shipobj.span.get_text() + shipobj.get_text()
                        # print("shipping==>", dic['shipping'])
                        # stomsg = li.find("div", attrs={"data-test" : "LPFulfillmentSectionStoreFA_storeMessaging"})
                        # if stomsg is not None :
                        #     nearby = li.find("div", attrs={"data-test" : "LPFulfillmentSectionStoreFA_checkNearbyStores"})
                        #     if ( nearby is not None):
                        #         dic['boston'] = stomsg.div.div.get_text()
                        #     # else:
                        #     #     dic['limit'] = stomsg.span.get_text() + stomsg.get_text()
                        # print("boston-->", dic['boston'])
                        # outmsg = li.find("div", attrs={"data-test": "LPFulfillmentSectionStoreFA_OPUMessaging"})
                        # if outmsg is not None : dic['limit'] = outmsg.span.get_text() + outmsg.get_text()
                        # print("outmsg==>", dic['limit'])
                        dic["source"] = config.sources["target"]
                        print("source==>", dic['source'])
                        self.goodlist.append(dic)
                        total+=1
                        print("total-->", total)
                        if ( total >= config.max_items):
                            print("target.com   ",  total)
                            self.first_driver.quit()
                            return 

                except Exception as e:
                    print("target.com   ",  total)
                    self.first_driver.quit()
                    return 

                pagenation = soup.find(class_="Link-sc-1khjl8b-0 bTKAgl Button-bwu3xu-0 CIgEw ButtonWithArrow-sc-6wuvfc-0 eDtmxH")
                if ( pagenation is not None):
                    nextbtn = self.first_driver.find_element_by_xpath("//a[@class='Link-sc-1khjl8b-0 bTKAgl Button-bwu3xu-0 CIgEw ButtonWithArrow-sc-6wuvfc-0 eDtmxH']")
                    nextbtn.click()
                    time.sleep(2)
                else:
                    print("target.com   ",  total)
                    self.first_driver.quit()
                    return

        except Exception as e:
            self.first_driver.quit()
            print("ERROR in target")
            print(e)

    def open_chrome(self):
    
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("enable-automation")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--proxy-server=us.smartproxy.com:10000" )
        # options.add_argument("--remote-debugging-port=9231")
        # _driver = webdriver.Chrome(options=options)
        _driver = webdriver.Chrome(options=options, executable_path='scrapers/chromedriver.exe')
        _driver.set_page_load_timeout(config.max_duration)
    
        
        return _driver

