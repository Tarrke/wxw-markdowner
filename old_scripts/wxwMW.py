#!/usr/bin/env python3
# coding: utf-8

from wxwMarkdowner import WXWMarkdowner
import os
import argparse

parser = argparse.ArgumentParser(description="Martial World Downloader and Ebook maker")
parser.add_argument("-b", "--begin", help="what chapter to begin the book with", type=int)
parser.add_argument("-e", "--end", help="what chapter to end the book with", type=int)
parser.add_argument("-t", "--title", help="Title of the Ebook", required=True)
parser.add_argument("-f", "--filename", help="Output filename", required=True)
args = parser.parse_args()

# No options called:
begin = 1
end = 100
if args.begin:
    begin = args.begin
if args.end:
    end = args.end

myMarkdowner = WXWMarkdowner(args.filename, args.title, "https://www.wuxiaworld.com/novel/martial-world", "")
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