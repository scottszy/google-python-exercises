#!/usr/bin/python3
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib
import urllib.request

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""

    path_list =  []      #list of urls to detect duplicates
    url_paths = []      #list for full url paths

    hostname_match = re.search(r'_(\S+)', filename)
    hostname = hostname_match.group(1)

    # Open and read entire file to string var
    f = open(filename, 'rt')

    # Find all puzzle files and hostnames and load into dictionary
    for line in f:
        # check for pattern in "place" file
        #place_match = re.search(r'\S+-(\w+)-(\w+.jpg)', line)

        path_match = re.search(r'\S+puzzle\S+', line)

        if path_match:
            path = path_match.group()

            if path not in path_list:
                url_paths.append('http://' + hostname + path)
                path_list.append(path)       #Update list to check for duplicates

    if re.search(r'\S+-(\w+)-(\w+.jpg)', url_paths[0]):
        sorted_url_paths = sorted(url_paths, key=lambda x: x[-8:-4])
    else:
        sorted_url_paths = sorted(url_paths)
    del path_list

    return sorted_url_paths

def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # make index.html file
    html_file = os.path.join(dest_dir, 'index.html')
    f = open(html_file, 'w')

    # start building html index
    f.write('<html>\n<body>\n')

    # download image into specified directory
    for url in img_urls:
        # create unique filename and find abs path
        filename = 'img' + str(img_urls.index(url)) + '.jpg'
        abs_path = os.path.abspath(os.path.join(dest_dir, filename))

        # Retrieve images
        print ('Retrieving...:\t%s \t->\t%s' % (filename, abs_path))
        #
        #<img src="/edu/python/exercises/img0">
        html_content = '<img src="' + abs_path + '">'
        f.write(html_content)
        urllib.request.urlretrieve(url, abs_path)

    # finish index file
    f.write('\n<html>\n<body>')
    f.close()

    return

def main():
    args = sys.argv[1:]

    if not args:
        print('usage: [--todir dir] logfile ')
        sys.exit(1)

    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    img_urls = read_urls(args[0])

    if todir:
        download_images(img_urls, todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main()
