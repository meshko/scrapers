# http://gazeta.zn.ua/authors/stanislav-vasin

from bs4 import BeautifulSoup
import urllib2
import sys
from urlparse import urlparse

base_url = sys.argv[1]

links_set = set()
response = urllib2.urlopen(base_url)
html = response.read()
soup = BeautifulSoup(html, 'html.parser')   
for h2 in soup.find_all("h2", class_="title"):
   links_set.add(h2.find("a")["href"])

purl = urlparse(base_url)
baser_url = purl.scheme + "://" + purl.netloc 
number = 1
for link in links_set:
   print baser_url+ link
   response = urllib2.urlopen(baser_url + link)
   html = response.read()
   #print html
   soup = BeautifulSoup(html, 'html.parser')
   f = open('file-%d.txt' % number, 'wb')
   number = number + 1   
   f.write(soup.find("h1", class_="title  ").get_text().encode("UTF-8")) 
   f.write("\n")
   #f.write(soup.find("a", class_="author_").get_text().encode("UTF-8"))
   #f.write("\n")
   f.write(soup.find("div", class_="date").get_text().encode("UTF-8"))
   f.write("\n")
   f.write(soup.find("div", class_="article_bd").get_text().encode("UTF-8"))
   f.close()
   print "processed file %d out of %d" % (number-1, len(links_set))
