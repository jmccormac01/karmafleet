"""
Search the forums for bazaar entries
"""
import os
import re
from html.parser import HTMLParser
from collections import defaultdict
import glob as g
import argparse as ap
import numpy as np

class MyParser(HTMLParser):
    def __init__(self, output_list=None):
        HTMLParser.__init__(self)
        if output_list is None:
            self.output_list = []
        else:
            self.output_list = output_list
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.output_list.append(dict(attrs).get('href'))

def argParse():
    """
    Parse the command line arguments
    """
    p = ap.ArgumentParser()
    p.add_argument('username',
                   help='name of user to search for')
    p.add_argument('n_pages',
                   type=int,
                   help='number of pages to check for')
    return p.parse_args()

if __name__ == "__main__":
    args = argParse()
    args.username = args.username.replace(' ', '%20')
    base_url = "http://eve-search.com/search/author"
    pages = np.arange(1, args.n_pages+1, 1)
    for page in pages:
        search_url = "{}/{}/page/{}".format(base_url, args.username, page)
        out_file = "{}_{:02d}.txt".format(args.username, page)
        os.system('wget {} -O {}'.format(search_url, out_file))

    hp = MyParser()

    links = []
    store = defaultdict(list)
    page_list = sorted(g.glob("{}*".format(args.username)))
    for page in page_list:
        ff = open(page, 'rb').readlines()
        for line in ff:
            if b"in Character Bazaar" in line:
                store[page].append(re.sub("<.*?>", "", str(line)))
                hp.feed(str(line))
                res = hp.output_list
                for r in res:
                    if "/thread/" in r:
                        thread_link = "https://eve-search.com/thread/{}".format(r.split('/')[2])
                        links.append(thread_link)
    links = set(links)

    print("Results from scraped pages for 'in Character Bazaar', posted by {}:".format(args.username))
    for page in store:
        for line in store[page]:
            print('{}: {}'.format(page, line))

    print("Direct links to each thread:")
    for link in links:
        print(link)

