# wxw-markdowner

A simple markdowner for WXW websites

## Usage

```bash
$ ./wxwDownloader.py -h
usage: wxwDownloader.py [-h] -f CONFIGFILE [-b BOOKS [BOOKS ...]]

Martial World Downloader and Ebook maker

optional arguments:
  -h, --help            show this help message and exit
  -f CONFIGFILE, --configFile CONFIGFILE
                        Configuratin file to run
  -b BOOKS [BOOKS ...], --books BOOKS [BOOKS ...]
                        Books to make, space separated list. Refers to the
                        json configuration file.
```

Example:

```bash
$ ./wxwDownloader.py -f MW.json -b 1 2 3 4
(...)
Compile the md file into an epub:
pandoc "/home/xxx/.cache/WXW/md/wxw-mw.md" --epub-stylesheet="epub-md.css" --toc --toc-depth=2 -o "/home/xxx/Documents/Epubs/WXW-wxw-mw.epub"
```

## ToDo

* Correct the output filename if books are passed as an option
* add some debug mode with verbose level
* fix the import warning

## Done

* ~Load the good markdowner~
* ~do a simple help menu~
* ~parse arguments when launched~
* ~make configuration file reading~

## Unit tests

~~~ bash
python3 -m unittest discover -v -s tests
~~~
