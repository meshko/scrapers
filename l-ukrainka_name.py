#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
# import csv
from bs4 import BeautifulSoup
# from urllib.request import urlopen
from urllib2 import urlopen
import codecs
import re
import unicodecsv as csv

base_urls = ["http://www.l-ukrainka.name/uk/Prose.html", "http://www.l-ukrainka.name/uk/Publicistics.html",
             "http://www.l-ukrainka.name/uk/Criticism.html", "http://www.l-ukrainka.name/uk/Corresp.html"]
author = u"Леся Українка"

def clear_unicode_string(s):
    control_chars = ''.join(map(unichr, range(0, 32) + range(127, 160)))
    control_char_re = re.compile('[%s]' % re.escape(control_chars))
    return control_char_re.sub('', s)


def do_bs4(url):
    name = re.sub("^.*/([^.]*).*", "\\1", url)
    print name
    name = "LU/" + name
    if not os.path.exists(name): os.makedirs(name)
    response = urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all("p", class_="BT")
    menu_links = soup.find_all("p", class_="Menu1")

    # remove links which don't actually have links before counting
    for link in links:
        aelt = link.find("a")
        if not aelt:
            links.remove(link)

    if len(menu_links) > len(links):
        links = menu_links
    for link in links:
        aelt = link.find("a")
        if not aelt:
            continue  # some texts are missing?
        if 'title' in aelt.attrs:
            linkname = clear_unicode_string(aelt['title'] + aelt.next_sibling.string)  # extract silly date
        else:
            linkname = aelt.text
            if linkname == '+':
                linkname = aelt.parent.next_sibling.text
        process_item(linkname, aelt['href'], name)


def get_text(body_elt):
    text = body_elt.text
    idx = text.rfind(u"Примітки")
    if idx == -1:
        idx = text.rfind(u"Попередній твір")
    return text[:idx]


def get_body_and_menu_elts(url):
    response = urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find("td", id="Stuff")
    menu = soup.find("div", class_="TreeDiv")
    return body, menu


def process_item(title, url, section_path):
    body, menu = get_body_and_menu_elts(url)

    # see if this is a multi-part page
    links = menu.find_all("p", class_="Menu")
    if not links:
        text = get_text(body)
    else:
        print "multi part", title
        text = ""
        for link in links:
            aelt = link.find("a")
            subbody, _ = get_body_and_menu_elts(aelt['href'])
            text += get_text(subbody)

    # silly way to extract year from the title
    date = re.findall("[0-9]{4}", title)
    if date:
        date = date[0]
    else:
        date = ""

    print title, date
    filename = section_path + "/" + title + ".txt"
    with codecs.open(filename, "w", "utf-8-sig") as outfile:
        outfile.write(text)
    with open(author+".csv", "a") as csvfile:
        csvwriter = csv.writer(csvfile, encoding='utf-8')
        csvwriter.writerow([author, title, filename, date, len(text)])


if __name__ == "__main__":
#    do_bs4(base_urls[3])
    for url in base_urls:
        do_bs4(url)
