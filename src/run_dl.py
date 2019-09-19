#!/usr/bin/env python3
# coding: utf-8

import os
import urllib.request
import bs4 as bs
from tomd import Tomd
import io
import shutil


def download_file(url, file_name):
    """Download a file from an url an record it on the disk."""
    request = urllib.request.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11')
    with urllib.request.urlopen(request) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    return out_file


if __name__ == "__main__":
    download_file("https://www.wuxiaworld.com/novel/martial-god-asura/mga-chapter-1", "result.html")
    download_file("https://www.wuxiaworld.com/novel/martial-world/mw-chapter-1505", "result.html")