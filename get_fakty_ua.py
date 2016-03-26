# http://fakty.ua/search?query=%D0%90%D0%BD%D0%BD%D0%B0+%D0%92%D0%BE%D0%BB%D0%BA%D0%BE%D0%B2%D0%B0&cid=articles&sort=2&fd=4&fm=3&fy=1999&td=4&tm=3&ty=2016&ArticlesItem_page=9
# &ArticlesItem_page=9

from bs4 import BeautifulSoup
import urllib2
import sys
from urlparse import urlparse

def process_search_page(soup, links_set):
   links = soup.find("div", class_="items").find_all('a')
   found_new = False
   for link in links:
      url = link['href']
      if url not in links_set:
         links_set.add(url)
         found_new = True
   return found_new

base_url = sys.argv[1]

links_set = set()
number = 1
while True:
   response = urllib2.urlopen(base_url + "&ArticlesItem_page=" + str(number))
   number = number + 1
   html = response.read()
   soup = BeautifulSoup(html, 'html.parser')   
   if not process_search_page(soup, links_set):
     break
   #break
   print "processed %d results pages, found %d links" % (number-1, len(links_set))

purl = urlparse(base_url)
baser_url = purl.scheme + "://" + purl.netloc + "/"
number = 1
for link in links_set:
   response = urllib2.urlopen(baser_url + link)
   html = response.read()
   #print html
   soup = BeautifulSoup(html, 'html.parser')
   f = open('file-%d.txt' % number, 'wb')
   number = number + 1   
   f.write(soup.find("div", class_="tit_main_news").get_text().encode("UTF-8"))
   f.write("\n")
   f.write(soup.find("div", class_="tech_info").find("div", class_="fl_l").get_text().encode("UTF-8"))
   f.write("\n")
   f.write(soup.find(id="article_content").get_text().encode("UTF-8"))
   f.close()
   print "processed file %d out of %d" % (number-1, len(links_set))
