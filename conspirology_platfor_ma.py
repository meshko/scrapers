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


import unittest, time, re

class Sel(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = url
        self.verificationErrors = []
        self.accept_next_alert = True
    def test_sel(self):
        driver = self.driver
        delay = 3
        driver.get(self.base_url)
        #driver.find_element_by_link_text("All").click()
        prev_height = -1
        for i in range(1,100):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            height = self.driver.execute_script("return document.body.scrollHeight;")
            if height == prev_height:
               break
            prev_height = height
            time.sleep(4)
        html_source = driver.page_source
        data = html_source.encode('utf-8')
        return data
        

def get_html():
   driver = webdriver.Firefox()
   driver.implicitly_wait(30)
   base_url = url
   verificationErrors = []
   accept_next_alert = True
   delay = 3
   driver.get(base_url)
   #driver.find_element_by_link_text("All").click()
   prev_height = -1
   for i in range(1,100):
       driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
       height = driver.execute_script("return document.body.scrollHeight;")
       if height == prev_height:
          break
       prev_height = height
       time.sleep(2)
   html_source = driver.page_source
   data = html_source.encode('utf-8')
   driver.quit()
   return data


if __name__ == "__main__":
   html = get_html()
   links_set = set()
   soup = BeautifulSoup(html, 'html.parser')   
   for h2 in soup.find_all("a", class_="title"):
      links_set.add(h2["href"])
   
   #print len(links_set), links_set
   
   number = 1
   purl = urlparse(url)
   baser_url = purl.scheme + "://" + purl.netloc 
   for link in links_set:
      if not link.startswith("http"):
         link = baser_url + "/" + link
      print link
      response = urllib2.urlopen(link)      
      html = response.read()
      #print html
      soup = BeautifulSoup(html, 'html.parser')
      f = open('file-%d.txt' % number, 'wb')
      number = number + 1   
      f.write(soup.find("div", class_="post-wrapper").get_text().encode("UTF-8")) 
      f.write("\n")
      #f.write(soup.find("div", itemprop="author").find("a").get_text().encode("UTF-8"))
      #f.write("\n")
      #f.write(soup.find("time").get_text().encode("UTF-8"))
      #f.write("\n")
      #f.write(soup.find("div", itemprop="articleBody").get_text().encode("UTF-8"))
      f.close()
      print "processed file %d out of %d" % (number-1, len(links_set))
