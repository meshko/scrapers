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
import unittest, time, re
import getpass

def setup():
   global loggedin
   firefox_profile = webdriver.FirefoxProfile()
   firefox_profile.set_preference('permissions.default.image', 2)
   firefox_profile.set_preference('permissions.default.desktop-notification', 1)
   driver = webdriver.Firefox(firefox_profile=firefox_profile)
   driver.implicitly_wait(30)
   loggedin = False
   return driver

loggedin = False
POSTS_LIMIT = 4000

name = None

def get_html(driver, url, username, password, stop_class, posts_limit, timeout=120, time_limit=.5):   
   global loggedin, name
   #verificationErrors = []
   #accept_next_alert = True
   #delay = 3
   if not loggedin:
      base_url = "https://www.facebook.com/"
      print("will get", base_url, flush=True)
      driver.get(base_url)
      print("will log in as ", username, flush=True)
      try:
         driver.implicitly_wait(0)
         #print("looking for email field")
         elem = driver.find_element_by_id("email")
         #print("got email filed")
         elem.send_keys(username)
         elem = driver.find_element_by_id("pass")
         elem.send_keys(password)
         elem.send_keys(Keys.RETURN)      
         loggedin = True
         driver.implicitly_wait(60)
         driver.find_element_by_class_name("_4kny")
         print("done with logging in", flush=True)
      except NoSuchElementException:      
        pass    
   driver.implicitly_wait(timeout)
   #print(driver.find_element_by_class_name("_1k67 _cy7"))
   base_url = url
   try:
      driver.get(base_url)
   except:
      driver.get(base_url) # 1 retry enough?

   #driver.find_element_by_link_text("All").click()   
   prev_heights = []
   #for i in range(1,500000):
   sleep_time = .1
   results = []
   if not name: 
      try:
         name_elt = driver.find_element_by_id("fb-timeline-cover-name")
         if name_elt:
            alt_name = name_elt.driver.find_element_by_css_selector("span.alternate_name")
            if alt_name:
               driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", alt_name) 
            name = name_elt.text 
            print("got name " + name)  
      except:
         pass
   print("processing ", name, flush=True)
   while True:
      #print("will get height")
      try:
         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
         height = driver.execute_script("return document.body.scrollHeight;")             
         driver.implicitly_wait(0)
      except Exception as e:
         print("failed to scroll: ", e)
      end_elem = None
      try:
         #elem = driver.find_elements_by_class_name(stop_class)
         end_elem = driver.find_element_by_css_selector(stop_class)
         print("found element which is end?", elem.get_attribute('innerHTML'), flush=True)         
      except:
         pass
      try:          
         #elem = driver.find_element_by_css_selector("div._5pcr") # whole post with comments
         #elem = driver.find_element_by_css_selector("div._1dwg") # just the post (inside 5pcr)
         #elem = driver.find_element_by_css_selector("div._5x46") 
         #print(elem)

         elems = driver.find_elements_by_css_selector("div._1dwg") # just the post (inside 5pcr)
         if len(elems) > 5:
            for elem in elems[:max(1,len(elems)-2)]:
               name_elem = elem.find_element_by_css_selector("span.fwb")
               #print(name_elem)
               if (name_elem and name_elem.text == name) or not name: # name mismatch suggests someone else wrote on this wall
                  results.append(elem.get_attribute('innerHTML'))
               driver.execute_script('var element = arguments[0]; element.parentNode.parentNode.parentNode.parentNode.removeChild(element.parentNode.parentNode.parentNode);', elem)
            driver.execute_script("window.scrollTo(0, 0);")
         
         print("%d %f" % (len(results), sleep_time), flush=True)
         #driver.execute_script('alert(document.getElementsByClassName("_1dwg")[0])')
         #print(driver.execute_script('return document.getElementsByClassName("_1dwg")[0].remove();'))
         #driver.execute_script('var element = arguments[0]; element.parentNode.removeChild(element);', elem)         
         #driver.execute_script('var element = arguments[0]; alert(element);', elem)
         #print(elem.get_attribute('innerHTML'), flush=True)
         #driver.execute_script('var comments = document.getElementsByClassName("_4-u2"); for (var i=0, l=comments.length; i<l; i++) { var e = comments[i]; e.parentNode.removeChild(e); }')
      except:
         #print("Unexpected error:", sys.exc_info()[0], flush=True)
         pass 
      #time.sleep(120)
      prev_heights.append(height)
      if len(results) > posts_limit:
         print("too much!", flush=True)
         #time.sleep(120) # sleep here to examine the remanants of the DOM
         break
      if end_elem: 
         print("found end elem, stop", end_elem, flush=True)
         break
      if (len(prev_heights) >= 20):
         prev_heights = prev_heights[-20:]
         #print(last_n_elts, sleep_time, flush=True)
         if all(map(lambda x: x == prev_heights[0], prev_heights)): # all equals
            sleep_time += (time_limit/10.0)
            prev_heights = []
            if sleep_time >= time_limit: break
            try:
               driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
               driver.execute_script("window.scrollTo(0, 0);")
            except Exception as e:
               print("failed to scroll: ", e)
      #print("scrolled", height)
      time.sleep(sleep_time)      
   elems = driver.find_elements_by_css_selector("div._1dwg") # just the post (inside 5pcr)
   for elem in elems:
      name_elem = elem.find_element_by_css_selector("span.fwb")
      if name is None or (name_elem and name_elem.text == name):
         results.append(elem.get_attribute('innerHTML'))
   return results


if __name__ == "__main__":
   if len(sys.argv) < 3:
      username = input("your facebook username: ")
      password = getpass.getpass("password: ")
      url = sys.argv[1]
   else:
      username = sys.argv[1]
      password = sys.argv[2]
      url = sys.argv[3]
  
   author_profile = url[url.rindex('/')+1:]
   out_file_name = author_profile + ".txt" 
 
   driver = setup()

   postHtmls = get_html(driver, url, username, password, "div.sx_7b3bb5", POSTS_LIMIT) 
   driver.quit()
   # reset selenium?
   driver = setup()

   f = open(out_file_name, 'w', encoding='utf-8')   
   f.write("downloading %s\n" % url)
   num_posts = 0
   written_posts = 0
   for postHtml in postHtmls:
      #print(postHtml)
      #soup = BeautifulSoup(postHtml, 'html.parser')   
      #soup = BeautifulSoup('<html><body>' + postHtml + '</body></html>', 'html.parser')   
      soup = BeautifulSoup(postHtml, 'html.parser')   
      #name = soup.find(id="fb-timeline-cover-name").get_text()
      #print("getting fb feed for ", name, flush=True)  

      num_posts += 1
      continue_elt = soup.find("span", class_="text_exposed_link")
      if continue_elt:
         suburl = continue_elt.find("a")["href"]
         print("url: ", suburl, flush=True)
         if suburl == "#": # WHAT is this?
            continue
         if not suburl.startswith("/permalink.php") and not author_profile in suburl: continue
         sub_posts = get_html(driver, "http://www.facebook.com/" + suburl, username, password, "div.UFIReplyActorPhotoWrapper", 1, timeout=3, time_limit=.2)
         if len(sub_posts) != 1:
            print("ERROR: weird number of posts found?", len(sub_posts), suburl)
         if len(sub_posts) == 0:
            continue
         soup = BeautifulSoup(sub_posts[0], 'html.parser')
         #print(sub_posts[0], flush=True)
         #soup = subsoup.find("div", class_="_1dwg") # "_1dwg _1w_m _q7o")
      text_class = "_5pbx userContent _3576" # "_5pbx userContent"
      # _5pbx userContent _22jv _3576
      post_text = soup.find("div", class_=text_class)
      if not post_text: post_text = soup.find("div", class_="_5pbx userContent _22jv _3576")
      if not post_text: post_text = soup.find("div", class_="userContent")
      if not post_text or post_text.get_text() == '':
         #print("skipping no post text?: ", soup.get_text())
         #print("html: ", soup.prettify())
         #print("-----------------------------------")
         continue      
      date_elt = soup.find("abbr", class_="_5ptz")
      if date_elt:
         f.write(date_elt.get_text())
         f.write("\n")
      f.write(post_text.get_text()) 
      written_posts += 1
      f.write("\n\n")
      f.flush()
      print("processed post %d out of %d" % (num_posts, len(postHtmls)))
   print("wrote %d posts (some skipped; e.g. shares)" % written_posts)
   f.close()
   driver.quit()
