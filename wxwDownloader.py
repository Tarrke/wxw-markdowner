#!/usr/bin/env python3
# coding: utf-8

from wxwMarkdowner import WXWMarkdowner
import os
import argparse
import json

parser = argparse.ArgumentParser(description="Martial World Downloader and Ebook maker")
parser.add_argument("-f", "--configFile", help="Configuratin file to run", required=True)
parser.add_argument('-b', '--books', nargs='+', help='Books to make, space separated list. Refers to the json configuration file.')
args = parser.parse_args()

# No options called:
begin = 1
end = 100
filename = ""
author = ""
title = ""

print("Config File:", args.configFile)

with open(args.configFile) as json_data:
    data = json.load(json_data)
    # Non Required Options
    try:
        begin = data["begin"]
    except:
        pass
    try:
        end = data["end"]
    except:
        pass
    try:
        title = data["title"]
    except:
        pass
    try:
        author = data["author"]
    except:
        pass
    # Mandatory
    try:
        filename = data["filename"]
    except:
        print("You must provide a filename for this novel.")
        exit(1)

    if args.books:
        print("Overwritting options with books values")
        print(args.books)
        begin = data["books"][args.books[0]]["begin"]
        end   = data["books"][args.books[-1]]["end"]

print(begin)
print(end)
print(author)
print(title)

myMarkdowner = WXWMarkdowner(filename, title, "https://www.wuxiaworld.com/novel/martial-world", author)
myMarkdowner.generate_filenames()
myMarkdowner.generate_metadata()
myMarkdowner.download_index()

myMarkdowner.download_contents(begin=begin, end=end)

print('\n\n')
print("Compile the md file into an epub:")

import subprocess

#args = ['pandoc', myMarkdowner.outmd, '--epub-stylesheet="./epub-md.css"', '--toc', '--toc-depth=2', '-o', '"'+myMarkdowner.outEpub+'"']
#print(args)
#subprocess.call(args)

print('pandoc "' + myMarkdowner.outmd + '" --epub-stylesheet="epub-md.css" --toc --toc-depth=2 -o "' + myMarkdowner.outEpub + '"')

exit(0)