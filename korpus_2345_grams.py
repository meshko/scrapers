# -*- coding: utf-8 -*-

url = "http://conspirology.platfor.ma/"

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
import urllib2
import sys
from urlparse import urlparse
import codecs

import unittest, time, re

def get_html(driver, url, word):
   for win in driver.window_handles:
      driver.switch_to.window(win)
      driver.close()
   
   base_url = url
   driver.get(base_url)
   #driver.find_element_by_link_text("All").click()
   elem = driver.find_element_by_id("c0_lex1")  
   elem.send_keys(word.decode("utf-8"))
   elem.send_keys(Keys.RETURN)   
   
   while len(driver.window_handles) < 2:
      print "waiting"
   
   driver.switch_to.window(driver.window_handles[1])
   #WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body', '')))
   WebDriverWait(driver, 60).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body"), r"При цитировании примеров просим ссылаться".decode("utf-8")))   
   #print "loaded!"
   html_source = driver.page_source
   data = html_source.encode('utf-8')   
   return data


if __name__ == "__main__":
   f = open("words.txt", "r")
   words = f.readlines()
   f.close()
   driver = webdriver.Firefox()
   driver.implicitly_wait(30)   
   
   for word in words:
      word = word.strip('\r\n')
      print "processing word", word,
      for t in range(2,6):
         print t,
         sys.stdout.flush()
         html = get_html(driver, "http://ruscorpora.ru/search-ngrams_%d.html" % t, word)
         filename = "%s-%d.html" % (word.decode('utf-8'), t)
         with codecs.open(filename, "w", "utf-8-sig") as f:
            f.write(html.decode("utf-8"))
            f.close()
      print "done."
   driver.quit()