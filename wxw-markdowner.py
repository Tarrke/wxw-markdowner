#!/usr/bin/env python3
# coding: utf-8

"""
Cf README.md for the moment
"""

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

class WXWMarkdowner:
    """ Class for our Markdowner """

    def __init__(self, title, title_display, url):
        self.title = title
        self.title_display = title_display
        self.index_url = url
        #self.myopener = MyOpener()
        self.chap_limit = 5

    def generate_filenames(self):
        """ Generate the needed directories, files and names for thoses."""
        self.outDir = os.path.join( os.path.expanduser("~") , "Documents","Epubs" )
        if not os.path.exists(self.outDir):
            os.makedirs(self.outDir)
        self.outEpub = os.path.join( self.outDir, 'WXW-' + self.title + '.epub' )
        self.cachedir = os.path.join( os.path.expanduser("~"), '.cache', 'WXW')
        if not os.path.exists(self.cachedir):
            os.makedirs(self.cachedir)
        self.cachedirMD = os.path.join( os.path.expanduser("~"), '.cache', 'WXW', 'md')
        if not os.path.exists(self.cachedirMD):
            os.makedirs(self.cachedirMD)
        self.outmd = os.path.join(self.cachedirMD, self.title + '.md')
        if os.path.exists(self.outmd):
            os.remove(self.outmd)
        self.outmeta = os.path.join(self.cachedirMD, self.title + '.meta')
        if os.path.exists(self.outmeta):
            os.remove(self.outmeta)

        print("Directories & files")
        print("outDir   : ", self.outDir)
        print("outEpub  : ", self.outEpub)
        print("outMD    : ", self.outmd)
        print("cachedir : ", self.cachedir)

    def generate_metadata(self):
        """ Generates the metadata file """
        with open(self.outmeta, 'w') as f:
            print("Generating metadata file:", self.outmeta)
            f.write("<dc:title>" + self.title_display + "</dc:title>\n")
            f.write("<dc:language>en-US</dc:language>\n")
            f.write("<dc:creator opf:file-as=\"XXX\" opf:role=\"aut\">XXX</dc:creator>\n")
            f.write("<dc:publisher>" + self.index_url + "</dc:publisher>\n")
            f.write("<dc:publisher>Tarrke</dc:publisher>\n")
            f.write("<dc:description>" + self.title_display +" (from: www.wuxiaworld.com)</dc:description>\n")
            f.write("<dc:subject>Manwa Chinois</dc:subject>\n")
            msg="<dc:rights>Copyright ©2018 by http://www.wuxiaworld.com</dc:rights>\n"
            f.write(msg)

    def download_contents(self):
        """ Download all chapters then make a md file from them."""
        out = io.open(self.outmd, "w")

        # Mark some metadata here too
        out.write("---\n")
        out.write("title: "+self.title_display+"\n")
        out.write("author: Kindhearted Bee\n")
        out.write("language: en-US\n")
        out.write("...\n")
        out.write("\n")

        for chap in self.chaps:
            print("DL chapter", chap[0], ":", chap[2].strip())
            url = chap[1]
            num = int(chap[0])
            print("DL:", url)
            cacheFile = os.path.join(self.cachedir, 'WXW-' + self.title + '-chapter-' + str(num) + '.html')
            print("CacheFile: " + cacheFile)
            if not os.path.exists(cacheFile):
                print("Donwloading " + url)
                download_file(url, cacheFile)
            else:
                print("Using cache file")

            # Parsing the HTML file
            print("Parsing file...")
            html = open(cacheFile).read()
            soup = bs.BeautifulSoup(html, "lxml")
            data = soup.find('div', attrs={"class":u"fr-view"})

            if data.find('strong'):
                chapName = data.find('strong').parent.text.encode('utf8').strip()
                data.strong.extract()
            elif data.find('b'):
                chapName = data.find('b').parent.text.encode("utf8").strip()
                data.b.extract()
            else:
                print('Cant find the title')
                exit(1)

            # chapName.encode('utf-8')
            print("Title:", chapName)
            out.write(u"# "+chapName.decode('utf-8'))
            out.write('\n')

            for p in data.find_all('p'):
                if p.text == '' or p.text.startswith("Chapter") or p.text.startswith("Prologue") or p.text.startswith("Previous Chapter"):
                    p.extract()

            for a in data.find_all('a', attrs={"class":"chapter-name"}):
                a.extract()

            for hr in data.find_all('hr'):
                hr.extract()

            d = str(data)

            out.write( Tomd( d ).markdown )
            out.write( '\n' )
            print("")
        out.close()

    def download_index(self):
        """ Download index file and analyse it so we can get the chapters urls """
        download_file(self.index_url, "tmp")

        html = open("tmp").read()
        soup = bs.BeautifulSoup(html, 'lxml')
        data = soup.find_all('a')
        self.chaps = []
        cmpt = 1
        for link in data:
            if link.text.strip().startswith("Chapter") and not link.text.strip().startswith("Chapters"):
                # print "append chapter"
                self.chaps.append((cmpt,'http://wuxiaworld.com' + link['href'],link.text.strip()))
                cmpt += 1
            if self.chap_limit > 0 and cmpt > self.chap_limit:
                break
        print( self.chaps )

if __name__ == "__main__":
    print("Main things happening")

    myMarkdowner = WXWMarkdowner("MartialGodAsura", "Martial God Asura", "https://www.wuxiaworld.com/novel/martial-god-asura")
    myMarkdowner.generate_filenames()
    myMarkdowner.generate_metadata()
    myMarkdowner.download_index()
    myMarkdowner.download_contents()

    print('\n\n')
    print("Compile the md file into an epub:")
    print("pandoc " + myMarkdowner.outmd + ' --epub-metadata="' + myMarkdowner.outmeta + '" --epub-stylesheet="epub-md.css" --toc --toc-depth=2 -o "' + myMarkdowner.outEpub + '"')

    exit(0)