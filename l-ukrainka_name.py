#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import csv
from bs4 import BeautifulSoup
#from urllib.request import urlopen
from urllib2 import urlopen
import codecs
import re
import unicodedata

base_urls = ["http://www.l-ukrainka.name/uk/Prose.html", "http://www.l-ukrainka.name/uk/Publicistics.html",
             "http://www.l-ukrainka.name/uk/Criticism.html", "http://www.l-ukrainka.name/uk/Corresp.html"]


def clear_unicode_string(s):
    control_chars = ''.join(map(unichr, range(0, 32) + range(127, 160)))
    control_char_re = re.compile('[%s]' % re.escape(control_chars))
    return control_char_re.sub('', s)


def do_bs4(url):
    name = re.sub("^.*/([^.]*).*", "\\1", url)
    print name
    if not os.path.exists(name): os.mkdir(name)
    response = urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all("p", class_="BT")
    for link in links:
        aelt = link.find("a")
        if not aelt:
            continue  # some texts are missing?
        linkname = clear_unicode_string(aelt['title'] + aelt.next_sibling.string)  # extract silly date
        process_item(linkname, aelt['href'], name)


def get_text(body_elt):
    text = body_elt.text
    idx = text.rfind(u"Примітки")
    if idx == -1:
        idx = text.rfind(u"Попередній твір")
    return text[:idx]

def get_body_elt(url):
    response = urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find("td", id="Stuff")
    return body

def process_item(title, url, section):
    body = get_body_elt(url)

    # see if this is a multi-part page
    h3_elt = body.find("h3")
    links = h3_elt.find_all("a")
    if not links:
        text = get_text(body)
    else:
        print "multi part", title
        text = ""
        for link in links:
            subbody = get_body_elt(link['href'])
            text += get_text(subbody)

    print title
    with codecs.open(section + "/" + title + ".txt", "w", "utf-8-sig") as outfile:
        outfile.write(text)


if __name__ == "__main__":
  #do_bs4(base_urls[0])
  for url in base_urls[1:]:
    do_bs4(url)
