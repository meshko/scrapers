# -*- coding: utf-8 -*-
import os

base_url = "http://oldnewspapers.com.ua/"

from bs4 import BeautifulSoup
import urllib2
import sys
from urlparse import urlparse
import codecs
  

def do_bs4(newspaper):
  if not os.path.exists(newspaper): os.mkdir(newspaper)
  response = urllib2.urlopen(base_url + "/" + newspaper)  
  html = response.read()
  soup = BeautifulSoup(html, 'html.parser')   
  links = soup.find_all("div", class_="ts-pos")
  for link in links:
    aelt = link.find("a")
    process_day(newspaper, aelt['href'], aelt.text)

def process_day(newspaper, link, day):
  #print  "processing", day
  response = urllib2.urlopen(base_url + "/" + link)  
  html = response.read()
  soup = BeautifulSoup(html, 'html.parser')   
  links = soup.find_all("a", class_="link-style")
  for link in links:
    process_article(newspaper, link['href'], day, link['title'])

def process_article(newspaper, link, day, title):
  response = urllib2.urlopen(base_url + "/" + link)  
  html = response.read()
  soup = BeautifulSoup(html, 'html.parser')   
  body = soup.find("div", class_="story-content")
  with codecs.open(newspaper + "/" + title + ".txt", "w", "utf-8-sig") as f:
    f.write(body.text)
  cstr = newspaper + "," + title +  "," + day + "," + str(len(body.text)) + "\n"
  #print cstr.encode('utf-8')
  sys.stdout.write(cstr.encode('utf-8'))
  sys.stdout.flush()

if __name__ == "__main__":
  try:
    for np in ["hliborob", "shliakhdovoli", "dilo", "strilets"]: # "visti_vucvk"]:
      do_bs4(np)
  except:
    e = sys.exc_info()
    print "error: ", e
