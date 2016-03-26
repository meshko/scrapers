# http://nv.ua/opinion/bilinskiy.html

from bs4 import BeautifulSoup
import urllib2
import sys
from urlparse import urlparse

base_url = sys.argv[1]

links_set = set()
response = urllib2.urlopen(base_url)
html = response.read()
soup = BeautifulSoup(html, 'html.parser')   
for h2 in soup.find_all("div", class_="text"):
   links_set.add(h2.find("a")["href"])

purl = urlparse(base_url)
baser_url = purl.scheme + "://" + purl.netloc 
number = 1
for link in links_set:
   response = urllib2.urlopen(baser_url + link)
   print baser_url+ link
   html = response.read()
   #print html
   soup = BeautifulSoup(html, 'html.parser')
   f = open('file-%d.txt' % number, 'wb')
   number = number + 1   
   f.write(soup.find("h1", itemprop="headline").get_text().encode("UTF-8")) 
   f.write("\n")
   f.write(soup.find("div", itemprop="author").find("a").get_text().encode("UTF-8"))
   f.write("\n")
   f.write(soup.find("time").get_text().encode("UTF-8"))
   f.write("\n")
   f.write(soup.find("div", itemprop="articleBody").get_text().encode("UTF-8"))
   f.close()
   print "processed file %d out of %d" % (number-1, len(links_set))
