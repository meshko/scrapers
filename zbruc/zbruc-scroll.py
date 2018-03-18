#!/usr/bin/env python3

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
   driver = webdriver.Firefox(firefox_profile=firefox_profile)
   driver.implicitly_wait(30)
   return driver

loggedin = False
POSTS_LIMIT = 4000


def process_links(section_name, elt):
   pattern = re.compile("https://zbruc.eu/node/[0-9]*")
   links = elt.find_elements_by_tag_name("a")
   addrs = []
   for link in links:
      try:
         addr = link.get_attribute('href')
      except: 
         pass
      if not pattern.match(addr): continue
      addrs.append(addr)
   zg.process_files(section_name, addrs)


def get_html(driver, url):   
   driver.implicitly_wait(60)
   #print(driver.find_element_by_class_name("_1k67 _cy7"))
   base_url = url
   section_name = url.split('/')[-1]
   driver.get(base_url)

   prev_heights = []
   sleep_time = .1
   results = []
   count = 0

   left_sidebar_elt = driver.find_element_by_id('sidebar_left')
   right_sidebar_elt = driver.find_element_by_id('sidebar_right')
   driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", left_sidebar_elt)
   driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", right_sidebar_elt)

   while True:
      #print("will get height")
      bilshe_elts = driver.find_elements_by_css_selector("div.item-list")
      bilshe_elt = None
      idx = 0
      for be in bilshe_elts:
         if be.text.strip() != '':
            bilshe_elt = be
            be.click()
            #print("["+ be.text + "]", idx)
            break
         idx += 1
      
      if bilshe_elt:  
         driver.execute_script("arguments[0].scrollIntoView(true);", bilshe_elt) 
         count = 0
      else:
         count += 1

      if count > 10:
         print("done scrolling!")
         with open(section_name + ".html", 'w') as fout:
            fout.write(driver.page_source)
         process_links(section_name, driver.find_element_by_id('main_content'))
         break
      time.sleep(sleep_time)     
      #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      #height = driver.execute_script("return document.body.scrollHeight;")             
      #driver.implicitly_wait(0)
      #prev_heights.append(height)
      #if (len(prev_heights) >= 20):
      #   prev_heights = prev_heights[-20:]
      #   #print(last_n_elts, sleep_time, flush=True)
      #   if all(map(lambda x: x == prev_heights[0], prev_heights)): # all equals
      #      sleep_time += .05
      #      prev_heights = []
      #      if sleep_time >= .4: break
      #      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      #      driver.execute_script("window.scrollTo(0, 0);")
      #print("scrolled", height)

   #elems = driver.find_elements_by_css_selector("div._1dwg") # just the post (inside 5pcr)
   #for elem in elems:
   #   name_elem = elem.find_element_by_css_selector("span.fwb")
   #   if name_elem and name_elem.text == name:
   #      results.append(elem.get_attribute('innerHTML'))
   return results


if __name__ == "__main__":
   driver = setup()
   try:
      postHtmls = get_html(driver, sys.argv[1]) # "https://zbruc.eu/75_years_ago") 
   finally:   
      driver.quit()
