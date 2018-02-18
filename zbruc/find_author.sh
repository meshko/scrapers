#!/bin/bash

AUTHOR=$1
#"Іван Франко"
mkdir -p "$AUTHOR"

grep "<div class=\"field field-name-field-author field-type-taxonomy-term-reference field-label-hidden\"><div class=\"field-items\"><div class=\"field-item even\">$AUTHOR" -rIi . > find.txt
cat find.txt | cut -d ":" -f 1 | grep -v "page=" > "files-$AUTHOR.txt"
wc -l files.txt
./zbruc.py "files-$AUTHOR.txt" "$AUTHOR"
