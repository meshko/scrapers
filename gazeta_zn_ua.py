# http://gazeta.zn.ua/authors/stanislav-vasin
# http://gazeta.zn.ua/search/%D0%B2%D0%B8%D1%82%D0%B0%D0%BB%D0%B8%D0%B9%20%D0%BF%D0%BE%D1%80%D1%82%D0%BD%D0%B8%D0%BA%D0%BE%D0%B2
# 

from bs4 import BeautifulSoup
import urllib2
import sys
from urlparse import urlparse

def add_links(url, links):
   #print "looking for links on ", url
   response = urllib2.urlopen(url)
   html = response.read()
   soup = BeautifulSoup(html, 'html.parser')   
   found_new = False
   for h2 in soup.find_all("h2", class_="title"):
      link = h2.find("a")["href"]
      #print link
      if link not in links_set:
         links_set.add(link)
         found_new = True
   return found_new

if __name__ == "__main__":
   base_url = sys.argv[1]
   
   links_set = set()
   count = 1
   while add_links(base_url + "?page=" + str(count), links_set):
      count = count + 1
   
   purl = urlparse(base_url)
   baser_url = purl.scheme + "://" + purl.netloc 
   number = 1
   for link in links_set:
      if not link.startswith("http"):
         url = baser_url+ link
      else:
         url = link
      print url
      response = urllib2.urlopen(url)
      html = response.read()
      #print html
      soup = BeautifulSoup(html, 'html.parser')
      f = open('file-%d.txt' % number, 'wb')
      number = number + 1   
      title_elt = soup.find("h1", class_="title  ")
      if not title_elt:
         title_elt = soup.find("h1", class_="title zn ")
      f.write(title_elt.get_text().encode("UTF-8")) 
      f.write("\n")
      #f.write(soup.find("a", class_="author_").get_text().encode("UTF-8"))
      #f.write("\n")
      f.write(soup.find("div", class_="date").get_text().encode("UTF-8"))
      f.write("\n")
      body_elt = soup.find("div", class_="article_bd")
      if not body_elt:
         body_elt = soup.find("div", class_="article_body")
      f.write(body_elt.get_text().encode("UTF-8"))
      f.close()
      print "processed file %d out of %d" % (number-1, len(links_set))
