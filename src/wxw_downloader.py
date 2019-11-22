#!/usr/bin/env python3
# coding: utf-8

"""
    wxw_downloader

    wrapping script to use my markdowner.
"""

import argparse
import json
from wxw_markdowner import WXWMarkdowner
from wco_markdowner import WCOMarkdowner


def main():
    """ main function """
    # pylint: disable=too-many-statements
    parser = argparse.ArgumentParser(description="Martial World Downloader and Ebook maker")
    parser.add_argument("-f", "--configFile", help="Configuratin file to run", required=True)
    parser.add_argument('-b', '--books', nargs='+', help=
                        'Books to make, space separated list. Refers to the json configuration file'
                        )
    args = parser.parse_args()

    # No options called:
    begin = 1
    end = 100
    filename = ""
    author = ""
    title = ""
    starts = ["Chapter"]
    nostarts = ["Chapters"]

    print("Config File:", args.configFile)

    with open(args.configFile) as json_data:
        data = json.load(json_data)
        # Non Required Options
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
        # Mandatory
        try:
            filename = data["filename"]
        except KeyError:
            print("You must provide a filename for this novel.")
            exit(1)

        if args.books:
            print("Overwritting options with books values")
            print(args.books)
            begin = data["books"][args.books[0]]["begin"]
            end = data["books"][args.books[-1]]["end"]

    print(begin)
    print(end)
    print(author)
    print(title)

    print(url)

    # How to get the Right Markdowner ???
    my_markdowner = WXWMarkdowner(filename, title, url, author)
    my_markdowner.generate_filenames()
    my_markdowner.generate_metadata()
    my_markdowner.download_index(starts, nostarts)

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
