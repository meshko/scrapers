#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import datetime
import os
from bs4 import BeautifulSoup
import codecs
import re
import csv
from transliterate import translit
import urllib
import urllib.request
import unicodedata
import chardet

def is_cyrillic(text):
    count_cyrillic = 0
    count_latin = 0
    for c in text:
        try:
            if "CYRILLIC" in unicodedata.name(c):
                count_cyrillic += 1
            if "LATIN" in unicodedata.name(c):
                count_latin += 1
        except:
            pass
    return count_cyrillic >= .3 * (count_latin + count_cyrillic)


def is_russian(text):
    for c in text:
        if c in 'ҐґЇїЄє': return False
        if c in 'ЁёЫыЭэ': return True
    return True


def filter_valid_path(path_element):
    result = ""
    for c in path_element:
        if c.isalnum() or c.isdigit() or c in [' ', '_', '-']:
            result += c
    return result


def make_filename(collection_name, title, idx=None):
    if idx:
       idx = "-" + str(idx)
    else:
       idx = ""
    out_filename = filter_valid_path(translit(collection_name, 'uk', reversed=True)) + "/" + filter_valid_path(translit(title, 'uk', reversed=True).replace('/', '_')[:64]) + idx + ".txt"
    return out_filename


def make_unique_filename(collection_name, title):
    out_filename = make_filename(collection_name, title)
    idx = 0
    while os.path.exists(out_filename):
        out_filename = make_filename(collection_name, title, idx)
        idx += 1
    return out_filename

# http://irshavanews.in.ua/novini/irshavshina/14789-meshkanec-rshavschini-obkrav-svogo-odnoselcya.html
# <h1 class="artcTitle"><span class="masha_index masha_index1" rel="1"></span>Мешканець Іршавщини обікрав свого односельця</h1>
# <ul class="artinfo"><li>23-02-2018, 16:09</li>
# <div class="fullcontent">
def process_file(url, collection_name, fout_csv): 
    try:
       content = urllib.request.urlopen(url).read()
    except:
       print("retrying")
       content = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(content, 'html.parser')
    title_elt = soup.find("h1", class_="artcTitle")
    title_str = title_elt.text.strip()

    print(chardet.detect(title_str.encode()))
    #os.exit(0)

    date1_elt = soup.find("ul", class_="artinfo")
    date_elt = date1_elt.find("li")
    date_str = date_elt.text.strip()
    year_match = re.search("[0-9]{4}", date_str)
    if year_match:
       year_text = year_match.group(0)
    else:
       now = datetime.datetime.now()
       year_text = str(now.year) # default to current year in case of 'Вчора, 19:33'

    content_elt = soup.find("div", class_="fullcontent")
    # stupid cleanup
    bad_elts = content_elt.findAll('a', style="display:none;")
    for elt in bad_elts: elt.decompose()
    full_text = content_elt.get_text("\n").strip()

    #print(date_str, year_text)
    #print(title_str)
    #print(full_text)

    if not is_cyrillic(full_text):
        print("skipping polish", title_str, url)
        return

    if is_russian(full_text):
        print("skipping russian", title_str, url)
        return

    out_filename = make_unique_filename(collection_name, title_str)
    csvwriter = csv.writer(fout_csv)
    csvwriter.writerow([collection_name, out_filename, title_str, year_text, url, len(full_text)])
    with open(out_filename, "w") as fout:
        fout.write(title_str + "\n")
        fout.write(full_text)

def process_files(section, files):
    if not os.path.exists(section): os.mkdir(section)
    with open(section + ".csv", "w") as fout:
        count = 1
        for file in files:
            print("processing %s %d out of %d" % (file, count, len(files)))
            process_file(file, section, fout)
            count += 1


def collect_links(url, links):
    print("collecting links from %s, so far got %d" % (url, len(links)))
    content = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(content, 'html.parser')
    divs = soup.findAll('div', class_="newsIn")
    for div in divs:
       links.append(div.find('a').get('href'))
    #pages_elt = soup.find('div', class_='pages')
    #if not pages_elt:
    #   print("hmmmmm")
    #   return
    #for link in pages_elt.findAll('a'):
    for link in soup.findAll('a'):
       if link.get_text() == 'наступна':
          collect_links(link.get('href'), links)

def main(url):
    links = []
    collect_links(url, links)
    if url[-1] == '/': url = url[:-1]
    section = url[url.rindex('/')+1:]
    process_files(section, links)

#    if not os.path.exists(section): os.mkdir(section)
#    with open(section + ".csv", "w") as fout:
#        process_file("zbruc.eu/node/76667.html", section, fout)

# http://irshavanews.in.ua/irshavshina
if __name__ == "__main__":
    main(sys.argv[1])

