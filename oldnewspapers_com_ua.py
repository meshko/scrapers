# -*- coding: utf-8 -*-
import os
import csv

base_url = "http://oldnewspapers.com.ua/"

from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys
import codecs
  

def do_bs4(newspaper):
  if not os.path.exists(newspaper): os.mkdir(newspaper)
  response = urlopen(base_url + "/" + newspaper)  
  html = response.read()
  soup = BeautifulSoup(html, 'html.parser')     
  name_elt = soup.find_all("td", class_="txtbig")[1]
  #print name_elt
  name = name_elt.text
  links = soup.find_all("div", class_="ts-pos")
  for link in links:
    aelt = link.find("a")
    process_day(name, newspaper, aelt['href'], aelt.text)

def process_day(name, newspaper, link, day):
  #print  "processing", day
  response = urlopen(base_url + "/" + link)  
  html = response.read()
  soup = BeautifulSoup(html, 'html.parser')   
  links = soup.find_all("a", class_="link-style")
  for link in links:
    process_article(name, newspaper, link['href'], day, link['title'])

def process_article(name, newspaper, link, day, title):
  response = urlopen(base_url + "/" + link)  
  html = response.read()
  soup = BeautifulSoup(html, 'html.parser')   
  body = soup.find("div", class_="story-content")
  filename = title + ".txt"
  path = newspaper + "/" + filename
  #with codecs.open(path, "w", "utf-8-sig") as f:
  #  f.write(body.text)
  
  #with codecs.open('out.csv', 'ab', "utf-8-sig") as csvfile:
  with open('out.csv', 'a') as csvfile:
    csvwriter = csv.writer(csvfile)
    #print([name.replace(' ', '-'), filename, len(body.text), name, title, path, "публіцистичний", "Name", "", "", day])
    csvwriter.writerow([name.replace(' ', '-'), filename, len(body.text), name, title, path, "публіцистичний", "Name", "", "", day])

if __name__ == "__main__":
#  try:
  for np in ["hliborob", "shliakhdovoli", "dilo", "strilets", "visti_vucvk"]:
    do_bs4(np)
#  except:
#    e = sys.exc_info()
#    print "error: ", e
