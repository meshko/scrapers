#!/bin/bash

wget \
     --recursive \
     -c \
     -N \
     --no-clobber \
     --html-extension \
     --convert-links \
     --domains zbruc.eu \
     --no-parent \
     --reject jpg \
         https://zbruc.eu/

#     #--page-requisites \

