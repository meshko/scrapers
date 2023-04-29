#!/usr/bin/env python3
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException


from bs4 import BeautifulSoup
#import urllib2
from urllib.request import urlopen
from urllib.parse import urlparse
import sys
#from urlparse import urlparse
import time, re

import zbruc_gazeta as zg

def setup():
   firefox_profile = webdriver.FirefoxProfile()
   firefox_profile.set_preference('permissions.default.image', 2)
   driver = webdriver.Firefox(firefox_profile=firefox_profile, service_log_path=os.path.devnull)
   driver.implicitly_wait(30)
   return driver

def get_links(section_name, elt):
   pattern = re.compile("https://zbruc.eu/node/[0-9]*")
   links = elt.find_elements(By.TAG_NAME, "a")
   print(f"found {len(links)} links")
   addrs = []
   for link in links:
      try:
         addr = link.get_attribute('href')
      except: 
         pass
      if not pattern.match(addr): continue
      addrs.append(addr)
   print(f"found {len(addrs)} URLs")
   return addrs

def process_links(section_name, addrs):
   zg.process_files(section_name, addrs)


# from https://stackoverflow.com/questions/22702277/crawl-site-that-has-infinite-scrolling-using-python
def scroll_to_end():
  last_height = None
  while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(.5)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    #time.sleep(2)
    #break
    last_height = new_height

def get_html(driver, url):   
   driver.implicitly_wait(60)
   #print(driver.find_element_by_class_name("_1k67 _cy7"))
   base_url = url
   section_name = url.split('/')[-1]
   driver.get(base_url)

   #print("getting sidebars for some reason")
   #left_sidebar_elt = driver.find_element(By.ID, 'sidebar_left')
   #print("left", left_sidebar_elt)
   #right_sidebar_elt = driver.find_element(By.ID, 'sidebar_right')
   #print("right", right_sidebar_elt)
   #driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", left_sidebar_elt)
   #driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", right_sidebar_elt)

   scroll_to_end()

   print("done scrolling!")
   with open(section_name + ".html", 'w') as fout:
       fout.write(driver.page_source)
       main_elt = driver.find_element(By.ID, "isotope_items")
       #main_elt = driver.find_element(By.ID, "...")
       links = get_links(section_name, main_elt)
       driver.close()
       links = process_links(section_name, links)

if __name__ == "__main__":
   driver = setup()
   try:
      get_html(driver, sys.argv[1]) # "https://zbruc.eu/75_years_ago") 
   finally:   
      driver.quit()
