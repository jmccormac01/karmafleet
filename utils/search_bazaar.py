"""
Search the forums for bazaar entries
"""
import os
import re
from collections import defaultdict
import glob as g
import argparse as ap
import numpy as np

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

    store = defaultdict(list)
    page_list = sorted(g.glob("{}*".format(args.username)))
    for page in page_list:
        ff = open(page, 'rb').readlines()
        [store[page].append(re.sub("<.*?>", "", str(line))) for line in ff if b"in Character Bazaar" in line]

    print("Results from scraped pages for 'in Character Bazaar', posted by {}:".format(args.username))
    for page in store:
        for line in store[page]:
            print('{}: {}'.format(page, line))

