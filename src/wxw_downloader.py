#!/usr/bin/env python3
# coding: utf-8

"""
    wxw_downloader

    wrapping script to use my markdowner.
"""

import argparse
import json
import re
from wxw_markdowner import WXWMarkdowner # pylint: disable=unused-import
from wco_markdowner import WCOMarkdowner # pylint: disable=unused-import
from nf_markdowner  import NFMarkdowner  # pylint: disable=unused-import


def main():
    """ main function """
    # pylint: disable=too-many-statements
    parser = argparse.ArgumentParser(description="Martial World Downloader and Ebook maker")
    parser.add_argument("-f", "--configFile", help="Configuratin file to run", required=True)
    parser.add_argument('-b', '--books', nargs='+', help=
                        'Books to make, space separated list. Refers to the json configuration file'
                        )
    parser.add_argument("-t", "--title", help="Title of the Ebook if not the generic title in configuration file")
    args = parser.parse_args()

    # No options called:
    begin = 1
    end = 100
    filename = ""
    author = ""
    title = ""
    starts = ["Chapter"]
    nostarts = ["Chapters"]
    md_class = "WXWMarkdowner"
    find_chap = False

    print("Config File:", args.configFile)

    with open(args.configFile) as json_data:
        data = json.load(json_data)
        # Non Required Options
        try:
            md_class = data["mdClass"]
        except KeyError:
            pass
        try:
            begin = data["begin"]
        except KeyError:
            pass
        try:
            end = data["end"]
        except KeyError:
            pass
        try:
            title = data["title"]
        except KeyError:
            pass
        try:
            url = data["url"]
        except KeyError:
            pass
        try:
            author = data["author"]
        except KeyError:
            pass
        try:
            starts = data["starts"]
        except KeyError:
            pass
        try:
            nostarts = data["nostarts"]
        except KeyError:
            pass
        try:
            find_chap = data["findChap"]
            if find_chap:
                print("should print first chapter then exit...")
        except KeyError:
            pass
        # Mandatory
        try:
            filename = data["filename"]
        except KeyError:
            print("You must provide a filename for this novel.")
            exit(1)

    if args.books:
        print("~~ Overwritting options with books values")
        # print(args.books)
        begin = data["books"][args.books[0]]["begin"]
        end = data["books"][args.books[-1]]["end"]
        books_length = args.books.__len__()
        # print(books_length)
        if books_length > 0:
            title += " -- Book"
            if books_length > 1:
                title += "s"
            title += " "
            title += ",".join(args.books)

    if args.title:
        title = args.title

    print(begin)
    print(end)
    print(author)
    print(title)
    print(md_class)
    print(url)

    my_markdowner = eval(md_class)(filename, title, url, author) #pylint: disable=eval-used
    my_markdowner.generate_filenames()
    my_markdowner.generate_metadata()

    my_markdowner.download_index(starts, nostarts)
    print(my_markdowner.chaps[-1])

    if find_chap:
        p = re.compile('.*chapter 1 .*', re.IGNORECASE)
        for (c_id, c_link, c_title) in my_markdowner.chaps:
            if p.match(c_title):
                print(c_id, c_title)
            continue
        exit(0)

    my_markdowner.download_contents(begin=begin, end=end)

    print('\n\n')
    print("Compile the md file into an epub:")

    #import subprocess

    #args = ['pandoc', my_markdowner.outmd, '--css="./epub-md.css"',
    #        '--toc', '--toc-depth=2', '-o', '"'+my_markdowner.out_epub+'"']
    #print(args)
    #subprocess.call(args)

    print('pandoc "' + my_markdowner.outmd + '" --css="epub-md.css" --toc --toc-depth=2 -o "'
          + my_markdowner.out_epub + '"')

    exit(0)

if __name__ == '__main__':
    main()
