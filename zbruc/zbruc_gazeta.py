#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from bs4 import BeautifulSoup
import codecs
import re
import csv
from transliterate import translit
import urllib

no_name_idx = 0

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

    content_elt = soup.find("div", id="content")
    full_text = content_elt.text
    out_file_name = translit(collection_name, 'uk', reversed=True) + "/" + translit(title, 'uk', reversed=True) + ".txt"
    csvwriter.writerow([collection_name, out_file_name, title, publish_text, len(full_text), filename])
    with open(out_file_name, "w") as fout:
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
        process_file("zbruc.eu/node/76667.html", section, fout)

if __name__ == "__main__":
    main(sys.argv[1])

