# http://www.hesed-shpira.com.ua/2-news/145-2015-07-30-13-11-58
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import sys
from urlparse import urlparse

url = "http://www.hesed-shpira.com.ua/2-news/145-2015-07-30-13-11-58"

purl = urlparse(url)
baser_url = purl.scheme + "://" + purl.netloc 
number = 1
f = open('file.txt', 'wb')
while True:
   response = urllib2.urlopen(url)
   print url
   html = response.read()
   #print html
   soup = BeautifulSoup(html, 'html.parser')
   
   number = number + 1   
   text = soup.find("div", class_="item-page").get_text().encode("UTF-8")
   text = text.replace('< Назад', '')
   text = text.replace('Вперёд >', '')
   f.write(text) 
   f.write("\n")
   print "processed file %d" % (number-1)

   # find link to next page
   url = baser_url + soup.find("li", class_="pagenav-next").find("a")["href"]
f.close()
