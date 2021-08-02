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

BASE_URL = "https://www.dickssportinggoods.com/p/"
AFFILIATE_KEY = "dicks"

class Dickscom(Thread):
    def __init__(self, searchkey ):
        self.searchkey = searchkey
        self.first_driver = ''
        self.goodlist = []

        self.timeout = 30
        self.start_url = 'https://www.dickssportinggoods.com/search/SearchDisplay?searchTerm='
        
        if platform == "linux" or platform == "linux2":
                self.input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver")
        elif platform == "win32":
                self.input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver.exe")
        super(Dickscom, self).__init__()
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
            # if ( chrome is None ):
            #     self.first_driver.quit()
            #     print("dickssportinggoods.com : Access Denied.")
            #     return

            # self.first_driver.find_element_by_class_name("close").click()
            time.sleep(2)
            total = 0


            soup = BeautifulSoup( self.first_driver.page_source, "html.parser")
            obj = soup.find_all("div", class_="rs_product_card")

            if ( len(obj) == 0):
                print("dickssportinggoods.com : Please Enter Correct Key.")
                self.first_driver.quit()
                return

            for li in obj:
                dic ={}

                image = li.find('a', class_="image")
                if ( image is not None):
                    dic['image1'] = image.img['data-src']
                    # dic['detail'] = helpers.format_impact_affiliate_link("https://www.dickssportinggoods.com" + image['href'],BASE_URL,AFFILIATE_KEY)
                    dic['title'] = image['title']

                price = li.find("div", class_="rs_item_price")
                if ( price is not None ):
                    dic['price'] = helpers.strip_text_from_price(price.span.get_text())
                else: 
                    dic['price'] = ""

                dic["source"] = config.sources["dicks"]
                
                total += 1
                self.goodlist.append(dic)

                if ( total >= config.max_items):
                    print("dickssportinggoods.com:  " , total)
                    self.first_driver.quit()
                    return

            print("dickssportinggoods.com:  " , total)
            self.first_driver.quit()
            return
        except Exception as e:
            self.first_driver.quit()
            print("ERROR in dicks")
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
        # options.add_argument("--remote-debugging-port=9227")
        _driver = webdriver.Chrome(options=options, executable_path='scrapers/chromedriver.exe')
        _driver.set_page_load_timeout(config.max_duration)
        
        
        
        return _driver
