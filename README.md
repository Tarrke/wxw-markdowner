# wxw-markdowner

A simple markdowner for WXW websites

## Usage

```bash
$ ./wxwDownloader.py
usage: wxwDownloader.py [-h] -f CONFIGFILE [-b BOOKS [BOOKS ...]]
wxwDownloader.py: error: the following arguments are required: -f/--configFile
```

Example:

```bash
$ ./wxwGeneric.py -f MW.json -b 1 2 3 4
(...)
Compile the md file into an epub:
pandoc "/home/xxx/.cache/WXW/md/wxw-mw.md" --epub-stylesheet="epub-md.css" --toc --toc-depth=2 -o "/home/xxx/Documents/Epubs/WXW-wxw-mw.epub"
```

## ToDo

* ~do a simple help menu~
* ~parse arguments when launched~
* ~make configuration file reading~
* Correct the output filename if books are passed as an option