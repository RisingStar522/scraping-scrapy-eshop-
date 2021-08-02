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

BASE_URL = "https://www.sears.com/"
AFFILIATE_KEY = "sears"

class Searscom(Thread):
    def __init__(self, searchkey):
        self.searchkey = searchkey
        self.first_driver = ''
        self.goodlist = []
        self.timeout = 30
        self.start_url = 'https://www.sears.com/search='
        print("search key===>", searchkey)
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
            self.first_driver = self.open_chrome()
            self.first_driver.delete_all_cookies()
            chrome = self.first_driver.get(self.start_url + self.searchkey)
            # if (chrome is None):
            #     self.first_driver.quit()
            #     print( "Sears.com : Access Denied")
            #     return 
            time.sleep(5)

            total = 0
            
            while True:
                self.scroller(3)
                soup = BeautifulSoup( self.first_driver.page_source, "html.parser")
                obj = soup.find_all(class_="card-container card-border")

                if ( len(obj) == 0):
                    print("Sears.com : Please Enter Correct Key.")
                    self.first_driver.quit()
                    return

                for li in obj:
                    dic ={}
                    image = li.find(class_="card-image-height-content")
                    if ( image is not None):
                        dic['image1'] = image.img['ng-src']
                        # dic['detail'] = helpers.format_impact_affiliate_link("https://Sears.com/" + image['href'],BASE_URL,AFFILIATE_KEY)
                    print("image===>", dic['image1'])
                    price = li.find("span", class_="card-price-orig")
                    if ( price is not None ):
                        dic['price'] = li.get_text()
                    else: dic['price'] = "" 
                    print("price---->", dic['price'])

                    title = li.find("h3", class_="card-title")
                    if ( title is not None ):
                        dic['title'] = title.a.get_text()
                    else: dic['title'] = ""
                    print("title====>", dic['title'])

                    rate = li.find("span", attrs={"bo-if": "!!product.reviewCount"})
                    if ( rate is not None ):
                        dic['rate'] = rate.get_text()
                    else: dic['rate'] = ""
                    print("rate====>", dic['rate'])

                    shipmsg = li.find("span", attrs={"bo-text": "'Sold by ' + product.storeOrigin"})
                    if ( shipmsg is not None ):
                        dic['shipmsg'] = shipmsg.get_text()
                    else: dic['shipmsg'] = ""

                    shipping = li.find("span", attrs={"bo-text" : "product.bestDealMessage"})
                    if ( shipping is not None ):
                        dic['shipping'] = shipping.get_text()
                    else: dic['shipping'] = ""
                    print("shipping===>", dic['shipping'])

                    dic["source"] = "sears"
                    total += 1
                    print("total-------------------->,", total)
                    self.goodlist.append(dic)
                # print("SEARS ",total)
                    if ( total>=8):
                        print("sears.com:  " , total)
                        self.first_driver.quit()
                        return

                pagenation = soup.find("div", attrs={"ng-if" : "selectedPage.id < totalPages"})
                if ( pagenation is not None ):
                    nextbtn = self.first_driver.find_element_by_xpath("//div[@ng-if='selectedPage.id < totalPages']")
                    nextbtn.click()
                    time.sleep(2)
                else:
                    self.first_driver.quit()
                    print("Sears.com:  " , total)
                    return
        except Exception as e:
            self.first_driver.quit()
            print("ERROR in sears")
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
        # options.add_argument("--remote-debugging-port=9229")
        # _driver = webdriver.Chrome(chrome_options=options)
        _driver = webdriver.Chrome(options=options, executable_path='scrapers/chromedriver.exe')
        _driver.set_page_load_timeout(config.max_duration)
        
        
        return _driver








