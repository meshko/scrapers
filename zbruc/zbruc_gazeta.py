#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from bs4 import BeautifulSoup
import codecs
import re
import csv
from transliterate import translit
import urllib.request
import unicodedata

no_name_idx = 0

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

def process_file(filename, collection_name, fout_csv): 
    global no_name_idx
    csvwriter = csv.writer(fout_csv)
    if filename.startswith('http'):
       content= urllib.request.urlopen(filename).read()
       soup = BeautifulSoup(content, 'html.parser')
    else:
        with open(filename, 'r') as fin:
            soup = BeautifulSoup(fin, 'html.parser')
    title_elt = soup.find("div", id="page-title")
    title = title_elt.text.strip()
    if title[-1] == '.': title = title[:-1]
    if '◦' in title: 
       # well, this happens sometimes.
       title = "no name %d" % no_name_idx
       no_name_idx += 1

    publisher_elt = soup.find("div", class_="field-type-link-field")
    if publisher_elt:
        publisher = publisher_elt.text.strip()
    else:
        # do some acrobatics if not properly specified
        p_elts = soup.find_all("p")
        publisher  = ""
        for p_elt in p_elts:
            p_text = p_elt.text
            if len(p_text) > 2 and p_text[0] == '[' and p_text[-1] == ']':
                publisher = p_text[1:-1]
                break

    time_elt = soup.find("span", class_="date-display-single")
    time_text = time_elt.text.strip()

    publish_text = publisher + " " + time_text

    year_text = re.search("[0-9]{4}", time_text).group(0)

    content_elt = soup.find("div", id="content")
    #bad_div = content_elt.find("div", class_="field-name-field-date")
    #bad_div.decompose()a
    #for br in content_elt.find_all('br'):
    #    br.replace_with('\n')
    full_text = content_elt.get_text('\n')
    full_text = re.sub('\n+', '\n', full_text)

    if not is_cyrillic(full_text):
        print("skipping polish", title, publish_text, filename)
        return

    if is_russian(full_text):
        print("skipping russian", title, publish_text, filename)
        return

    out_filename = make_filename(collection_name, title)
    idx = 0
    while os.path.exists(out_filename):
        out_filename = make_filename(collection_name, title, idx)
        idx += 1
      
    csvwriter.writerow([collection_name, out_filename, title, publish_text, len(full_text), filename, publisher, year_text])
    with open(out_filename, "w") as fout:
        fout.write(full_text)

"""<div id="page-title" >""" # title
"""field-type-link-field """ # publisher
"""<span class="date-display-single" """ # date

def process_files(section, files):
    if not os.path.exists(section): os.mkdir(section)
    with open(section + ".csv", "w") as fout:
        count = 1
        for file in files:
            print("processing %s %d out of %d" % (file, count, len(files)))
            process_file(file, section, fout)
            count += 1


def main(section):
    if not os.path.exists(section): os.mkdir(section)
    with open(section + ".csv", "w") as fout:
        process_file("http://zbruc.eu/node/76667", section, fout)
        process_file("https://zbruc.eu/node/3329", section, fout)

if __name__ == "__main__":
    main(sys.argv[1])

