#!/usr/bin/env python3
# coding: utf-8

"""
    wxw_markdowner

    see README.md
"""

import os
import urllib.request
import io
import shutil
import bs4 as bs
from tomd import Tomd


def download_file(url, file_name):
    """Download a file from an url an record it on the disk."""
    request = urllib.request.Request(url)
    request.add_header('User-Agent',
                       ('Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) '
                        'Gecko/20071127 Firefox/2.0.0.11'))
    with urllib.request.urlopen(request) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    return out_file

class WXWMarkdowner:
    """ Class for our Markdowner """
    # pylint: disable=too-many-instance-attributes

    def __init__(self, title, title_display, url, author):
        self.title = title
        self.title_display = title_display
        self.index_url = url
        #self.myopener = MyOpener()
        # Set this if you want to set a hard limit on the chapter recuperation
        self.chap_limit = -1
        self.author = author
        self.out_dir = os.path.join(os.path.expanduser("~"), "Documents", "Epubs")
        self.out_epub = ""
        self.cachedir = ""
        self.cachedir_md = ""
        self.outmd = ""
        self.outmeta = ""
        self.chaps = []

    def generate_filenames(self):
        """ Generate the needed directories, files and names for thoses."""
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)
        self.out_epub = os.path.join(self.out_dir, 'WXW-' + self.title + '.epub')
        self.cachedir = os.path.join(os.path.expanduser("~"), '.cache', 'WXW')
        if not os.path.exists(self.cachedir):
            os.makedirs(self.cachedir)
        self.cachedir_md = os.path.join(os.path.expanduser("~"), '.cache', 'WXW', 'md')
        if not os.path.exists(self.cachedir_md):
            os.makedirs(self.cachedir_md)
        self.outmd = os.path.join(self.cachedir_md, self.title + '.md')
        if os.path.exists(self.outmd):
            os.remove(self.outmd)
        self.outmeta = os.path.join(self.cachedir_md, self.title + '.meta')
        if os.path.exists(self.outmeta):
            os.remove(self.outmeta)

        print("Directories & files")
        print("out_dir   : ", self.out_dir)
        print("out_epub  : ", self.out_epub)
        print("outMD    : ", self.outmd)
        print("cachedir : ", self.cachedir)
        print("MetaData : ", self.outmeta)

    def generate_metadata(self):
        """ Generates the metadata file """
        with open(self.outmeta, 'w') as opened_file:
            print("Generating metadata file:", self.outmeta)
            opened_file.write("<dc:title>" + self.title_display + "</dc:title>\n")
            opened_file.write("<dc:language>en-US</dc:language>\n")
            opened_file.write("<dc:creator opf:file-as=\"XXX\" opf:role=\"aut\">XXX</dc:creator>\n")
            opened_file.write("<dc:publisher>" + self.index_url + "</dc:publisher>\n")
            opened_file.write("<dc:publisher>Tarrke</dc:publisher>\n")
            opened_file.write("<dc:description>" + self.title_display +
                              " (from: www.wuxiaworld.com)</dc:description>\n")
            opened_file.write("<dc:subject>Manwa Chinois</dc:subject>\n")
            msg = "<dc:rights>Copyright ©2018 by http://www.wuxiaworld.com</dc:rights>\n"
            opened_file.write(msg)

    def download_contents(self, begin=None, end=None):
        """ Download all chapters then make a md file from them."""
        out = io.open(self.outmd, "w")

        print("Arg begin:", begin)
        print("Arg end:", end)

        # Mark some metadata here too
        out.write("---\n")
        out.write("title: "+self.title_display+"\n")
        out.write("author: "+self.author+"\n")
        out.write("language: en-US\n")
        out.write("...\n")
        out.write("\n")

        for chap in self.chaps:
            if begin and int(chap[0] < begin):
                continue
            if end and int(chap[0] > end):
                out.close()
                return
            print("DL chapter", chap[0], ":", chap[2].strip())
            url = chap[1]
            num = int(chap[0])
            print("DL:", url)
            cache_file = os.path.join(self.cachedir,
                                      'WXW-' + self.title + '-chapter-' + str(num) + '.html')
            print("cache_file: " + cache_file)
            if not os.path.exists(cache_file):
                print("Donwloading " + url)
                download_file(url, cache_file)
            else:
                print("Using cache file")

            # Parsing the HTML file
            print("Parsing file...")
            html = open(cache_file).read()
            soup = bs.BeautifulSoup(html, "lxml")
            data = soup.find('div', attrs={"class":u"panel-default"}
                            ).find('div', attrs={"class":u"fr-view"})
            chap_name = ''
            if data.find('strong'):
                print('title from strong')
                print(data.find('strong'))
                chap_name = data.find('strong').text.strip()
                data.strong.extract()
            elif data.find('b'):
                print('title from b')
                chap_name = data.find('b').text.strip()
                data.b.extract()
            else:
                # Maybe the title is a spoiler...
                if soup.find('h4', attrs={"class":"text-spoiler"}):
                    print('title from h4 (spoiler)')
                    chap_name = soup.find('h4', attrs={"class":"text-spoiler"}).text.strip()
                elif data.find('p').text.startswith("Chapter"):
                    chap_name = data.find('p').text
                    print("title from first line")
                    print(chap[2].strip())
                elif not chap_name:
                    print("title from index")
                    chap_name = chap[2].strip()
            # Hack pour la demande de fond d'un traducteur...
            if chap_name.startswith('Please'):
                chap_name = chap[2].strip()

            chap_name = chap_name.encode("utf8")

            print("Title:", chap_name)
            out.write(u"# "+chap_name.decode('utf-8'))
            out.write('\n')

            for paragraph in data.find_all('p'):
                if (paragraph.text == '' or paragraph.text.startswith("Chapter") or
                        paragraph.text.startswith("Prologue") or
                        paragraph.text.startswith("Previous Chapter")):
                    paragraph.extract()

            for alink in data.find_all('a', attrs={"class":"chapter-name"}):
                alink.extract()

            for hrules in data.find_all('hr'):
                hrules.extract()

            data_str = str(data)

            out.write(Tomd(data_str).markdown)
            out.write('\n')
            print("")
        out.close()

    def download_index(self, starts=["Chapter"], nostarts=["Chapters"]): # pylint: disable=dangerous-default-value
        """ Download index file and analyse it so we can get the chapters urls """
        file_name = "tmp"
        download_file(self.index_url, file_name)

        self.get_chapter_from_index(file_name, starts, nostarts)

    def get_chapter_from_index(self, file_name, starts=["Chapter"], nostarts=["Chapters"]):
        """ Get the chapter list from an html index file """
        # pylint: disable=dangerous-default-value
        print("get_chapter_from_index starts")
        with open(file_name, 'r') as opened_file:
            html = opened_file.read()
        soup = bs.BeautifulSoup(html, 'lxml')
        data = soup.find_all('a')
        self.chaps = []
        cmpt = 1

        for link in data:
            if (not link.parent.has_attr('class') or (link.parent.has_attr('class') and not
                                                      "chapter-item" in link.parent['class'])):
                # This is not a chapter link
                print("Skipped:", link.text.strip())
                continue
            if link.has_attr('role') and link['role'] == 'button':
                print("Skipped button:", link.text.strip())
                continue
            if (link.text.strip().startswith(tuple(starts)) and
                    not link.text.strip().startswith(tuple(nostarts))):
                # print "append chapter"
                self.chaps.append((cmpt, 'http://wuxiaworld.com' + link['href'], link.text.strip()))
                cmpt += 1
            else:
                print("Skipped:", link.text.strip())
            if self.chap_limit > 0 and cmpt > self.chap_limit:
                break

        print("get_chapter_from_index stops")

if __name__ == "__main__":
    print("Main things happening")

    MYMARKDOWNER = WXWMarkdowner("MartialGodAsura", "Martial God Asura",
                                 "https://www.wuxiaworld.com/novel/martial-god-asura", "")
    MYMARKDOWNER.generate_filenames()
    MYMARKDOWNER.generate_metadata()
    MYMARKDOWNER.download_index()
    MYMARKDOWNER.download_contents()

    print('\n\n')
    print("Compile the md file into an epub:")
    print("pandoc " + MYMARKDOWNER.outmd + ' --epub-metadata="' + MYMARKDOWNER.outmeta +
          '" --css="epub-md.css" --toc --toc-depth=2 -o "' + MYMARKDOWNER.out_epub + '"')

    exit(0)
