#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


__author__ = "DJJD2150, Jaspal Singh, Mike A., Kano Marvel, David R."


import os
import re
import sys
import urllib.request
import argparse


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    # opens a read-only version of the given log file
    with open(filename, 'r') as f:
        # reads the file and assigns it to a variable
        puzzles = f.read()
        # creates a variable and regex statement to search for matches of
        # the parts of the URLs that contain pieces of the puzzle image
        regex1 = r'/edu/languages/google-python-class/images/puzzle/.*jpg'
        # This list comprehension removes duplicate URLs by converting
        # the list to a set, and then back to a list again
        # Then it assigns the list to a variable and adds the part of the
        # URL not included in the regex statement
        final_urls = ["http://code.google.com" + url
                      for url in list(set(re.findall(regex1, puzzles)))]
        # sorts the URL by its specified part (i.e. the last one)
        # alphabetically using the split method
        final_urls.sort(key=lambda x: x.split('-')[-1])
    return final_urls


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    # Makes a new directory if it doesn't already exist
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    # Creates an empty string
    img_elements = ''
    # Loops through the image URLs in the list argument
    for index, img_url in enumerate(img_urls):
        # Makes sure the images are being retrieved by keeping progress
        # in the terminal
        print('Retrieving img' + str(index) + '...')
        # Adds the images to the string
        img_elements += f'<img src="img{index}.jpg" />'
        # Downloads the images
        urllib.request.urlretrieve(img_url, f'{dest_dir}/img{index}.jpg')

    # Creates an HTML file that puts together the parts of the images
    # to form the whole image, already pre-sorted in its correct order
    with open(dest_dir + '/index.html', 'w+') as file:
        file.write(f"""<html>
        <body>
        {img_elements}
        </body>
        </html>""")


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
