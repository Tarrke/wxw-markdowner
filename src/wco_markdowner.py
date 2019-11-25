#!/usr/bin/env python3
# coding: utf-8

"""
    wco_markdowner

    see README.md

    This should be deprecated, but not sure...
"""

import os
import urllib.request
import io
import shutil
import bs4 as bs


def download_file(url, file_name):
    """Download a file from an url an record it on the disk."""
    request = urllib.request.Request(url)
    request.add_header('User-Agent',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; ' +
                       'rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11')
    with urllib.request.urlopen(request) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    return out_file


class WCOMarkdowner:
    """ Class for our Markdowner """

    def __init__(self, title, title_display, url, author):
        self.title = title
        self.title_display = title_display
        self.index_url = url
        self.author = author
        # Set this if you want to set a hard limit on the chapter recuperation
        self.chap_limit = -1
        self.out_dir = ""
        self.out_epub = ""
        self.cachedir = ""
        self.cache_dir_md = ""
        self.outmd = ""
        self.outmeta = ""
        self.chaps = []

    def generate_filenames(self):
        """ Generate the needed directories, files and names for thoses."""
        self.out_dir = os.path.join(
            os.path.expanduser("~"), "Documents", "Epubs")
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)
        self.out_epub = os.path.join(self.out_dir, 'WXW-' + self.title + '.epub')
        self.cachedir = os.path.join(os.path.expanduser("~"), '.cache', 'WXW')
        if not os.path.exists(self.cachedir):
            os.makedirs(self.cachedir)
        self.cache_dir_md = os.path.join(
            os.path.expanduser("~"), '.cache', 'WXW', 'md')
        if not os.path.exists(self.cache_dir_md):
            os.makedirs(self.cache_dir_md)
        self.outmd = os.path.join(self.cache_dir_md, self.title + '.md')
        if os.path.exists(self.outmd):
            os.remove(self.outmd)
        self.outmeta = os.path.join(self.cache_dir_md, self.title + '.meta')
        if os.path.exists(self.outmeta):
            os.remove(self.outmeta)

        print("Directories & files")
        print("out_dir   : ", self.out_dir)
        print("out_epub  : ", self.out_epub)
        print("outMD    : ", self.outmd)
        print("cachedir : ", self.cachedir)

    def generate_metadata(self):
        """ Generates the metadata file """
        with open(self.outmeta, 'w') as fichier:
            print("Generating metadata file:", self.outmeta)
            fichier.write("<dc:title>" + self.title_display + "</dc:title>\n")
            fichier.write("<dc:language>en-US</dc:language>\n")
            fichier.write(
                "<dc:creator opf:file-as=\"XXX\" opf:role=\"aut\">XXX</dc:creator>\n")
            fichier.write("<dc:publisher>" + self.index_url + "</dc:publisher>\n")
            fichier.write("<dc:publisher>Tarrke</dc:publisher>\n")
            fichier.write("<dc:description>" + self.title_display +
                          " (from: www.wuxiaworld.co)</dc:description>\n")
            fichier.write("<dc:subject>Manwa Chinois</dc:subject>\n")
            msg = "<dc:rights>Copyright ©2018 by http://www.wuxiaworld.co</dc:rights>\n"
            fichier.write(msg)

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
            cache_file = os.path.join(
                self.cachedir, 'WXW-' + self.title + '-chapter-' + str(num) + '.html')
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
            data = soup.find('div', attrs={'id': 'content'})
            chapter_name = ''
            if data.find('strong'):
                print('title from strong')
                print(data.find('strong'))
                chapter_name = data.find('strong').text.strip()
                data.strong.extract()
            elif data.find('b'):
                print('title from b')
                chapter_name = data.find('b').text.strip()
                data.b.extract()
            else:
                # Maybe the title is a spoiler...
                if soup.find('h4', attrs={"class": "text-spoiler"}):
                    print('title from h4 (spoiler)')
                    chapter_name = soup.find(
                        'h4', attrs={"class": "text-spoiler"}).text.strip()
                # Maybe it's the first line ?
                clean_data = str(data)
                # pylint: disable=line-too-long
                clean_data = clean_data.replace('<br/>', '\n\n').replace('<div id="content">', '').replace('</div>', '').strip()
                s_title = clean_data.split('\n')[0].strip()
                if s_title.startswith('Chapter'):
                    chapter_name = s_title
            if chapter_name == "":
                # Let's try looking for div bookname
                book_name = soup.find('div', attrs={'class': 'bookname'}).find('h1').text
                print(book_name)
                if book_name != "":
                    print("Chapter title from bookname div")
                    chapter_name = 'Chapter ' + book_name
                else:
                    print("Chapter title from index")
                    chapter_name = 'Chapter ' + chap[2].strip()

            chapter_name = chapter_name.encode("utf8")

            print("Title:", chapter_name)
            out.write(u"# "+chapter_name.decode('utf-8'))
            out.write('\n')

            for script_mark in data.find_all('script'):
                script_mark.extract()
            for p_mark in data.find_all('p'):
                # pylint: disable=line-too-long
                if p_mark.text == '' or p_mark.text.startswith("Chapter") or p_mark.text.startswith("Prologue") or p_mark.text.startswith("Previous Chapter"):
                    p_mark.extract()

            for a_mark in data.find_all('a', attrs={"class": "chapter-name"}):
                a_mark.extract()

            for hr_mark in data.find_all('hr'):
                hr_mark.extract()

            clean_data = str(data)
            # pylint: disable=line-too-long
            clean_data = clean_data.replace('<br/>', '\n\n').replace('<div id="content">', '').replace('</div>', '').strip()

            for line in clean_data.split('\n'):
                if line.startswith('Chapter') or line.startswith('Translator'):
                    print("Skipped")
                    continue
                out.write(line)
                out.write('\n')
            out.write('\n')
            out.write('\n')

            print("")
        out.close()

    def download_index(self, starts=["Chapter"], nostarts=["Payup"]):
        """ Download index file and analyse it so we can get the chapters urls """
        download_file(self.index_url, "tmp")

        html = open("tmp").read()
        soup = bs.BeautifulSoup(html, 'lxml')
        data = soup.find('div', attrs={'id': 'list'})
        #print(data)
        data = data.find_all('a')
        #print(data)
        self.chaps = []
        cmpt = 1
        for link in data:
            # print "append chapter"
            self.chaps.append(
                (cmpt,
                 'http://wuxiaworld.co/Library-of-Heaven-is-Path/' + link['href'],
                 link.text.strip()))
            cmpt += 1
            if self.chap_limit > 0 and cmpt > self.chap_limit:
                break
        print(self.chaps)


if __name__ == "__main__":
    print("Main things happening")

    MY_MARKDOWNER = WCOMarkdowner("MartialGodAsura", "Martial God Asura",
                                  "https://www.wuxiaworld.com/novel/martial-god-asura", "")
    MY_MARKDOWNER.generate_filenames()
    MY_MARKDOWNER.generate_metadata()
    MY_MARKDOWNER.download_index()
    MY_MARKDOWNER.download_contents()

    print('\n\n')
    print("Compile the md file into an epub:")
    print("pandoc " + MY_MARKDOWNER.outmd + ' --epub-metadata="' + MY_MARKDOWNER.outmeta +
          '" --epub-stylesheet="epub-md.css" --toc --toc-depth=2 -o "'
          + MY_MARKDOWNER.out_epub + '"')

    exit(0)
