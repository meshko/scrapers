# "https://www.facebook.com/mikhail.kruk"

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
import getpass

def setup():
   driver = webdriver.Firefox()
   driver.implicitly_wait(30)
   return driver

def get_html(driver, url, username, password):
   base_url = url
   #verificationErrors = []
   #accept_next_alert = True
   #delay = 3
   #print "will get", base_url
   driver.get(base_url)

   #print "will log in as ", username
   try:
      driver.implicitly_wait(0)
      #print "looking for email field"
      elem = driver.find_element_by_id("email")
      #print "got email filed"
      elem.send_keys(username)
      elem = driver.find_element_by_id("pass")
      elem.send_keys(password)
      elem.send_keys(Keys.RETURN)      
   except NoSuchElementException:      
      pass 
   #print "done with logging in"
   driver.implicitly_wait(30)

   #driver.find_element_by_link_text("All").click()   
   prev_height = -1
   for i in range(1,500000):
       #print "will get height"
       driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
       height = driver.execute_script("return document.body.scrollHeight;")
       if height == prev_height:
          break
       prev_height = height
       print "scrolled", height
       time.sleep(.9)
   html_source = driver.page_source
   data = html_source.encode('utf-8')
   return data


if __name__ == "__main__":
   if len(sys.argv) < 3:
      username = raw_input("your facebook username: ")
      password = getpass.getpass("password: ")
      url = sys.argv[1]
   else:
      username = sys.argv[1]
      password = sys.argv[2]
      url = sys.argv[3]
   
   driver = setup()

   html = get_html(driver, url, username, password)
   soup = BeautifulSoup(html, 'html.parser')   
   
   name = soup.find(id="fb-timeline-cover-name").get_text()
   print "getting fb feed for ", name 

   f = open('file.txt', 'wb')
   for post in soup.find_all("div", class_="_1dwg"):
      continue_elt = post.find("span", class_="text_exposed_link")
      if continue_elt:
         suburl = continue_elt.find("a")["href"]
         print suburl
         if suburl == "#": # WHAT is this?
            continue
         #response = urllib2.urlopen("http://www.facebook.com/" + suburl)         
         #subhtml = response.read()
         #print html
         subhtml = get_html(driver, "http://www.facebook.com/" + suburl, username, password)
         subsoup = BeautifulSoup(subhtml, 'html.parser')
         post = subsoup.find("div", class_="_1dwg")
      #print post, '\n', post.get_text(), '------------------\n'
      name_elt = post.find("span", class_="fwb fcg")
      if not name_elt or name_elt.get_text() != name:
         print "skipping: ", post.get_text().encode("UTF-8")
         continue         
      post_text = post.find("div", class_="_5pbx userContent")
      if not post_text:
         print "skipping: ", post.get_text().encode("UTF-8")
         continue      
      date_elt = post.find("abbr", class_="_5ptz")
      if date_elt:
         f.write(date_elt.get_text().encode("UTF-8") + "\n")
      f.write(post_text.get_text().encode("UTF-8")) 
      f.write("\n\n")
   f.close()
   driver.quit()

