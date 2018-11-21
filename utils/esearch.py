"""
Search my Eve chat logs for a particular string
"""
import argparse as ap
import os
import platform

CHAT_LOGS_DIR = '/Users/jmcc/Documents/EVE/logs/Chatlogs/'

if 'win' in platform.system().lower():
    line_ending = '\r\n'
else:
    line_ending = '\n'

def arg_parse():
    """
    Parse the command line arguments
    """
    p = ap.ArgumentParser()
    p.add_argument('str_to_find',
                   help='string to find in EVE chatlogs')
    return p.parse_args()

if __name__ == "__main__":
    args = arg_parse()
    with open('results.txt', 'w') as of:
        os.chdir(CHAT_LOGS_DIR)
        chatlogs = [lf for lf in sorted(os.listdir('.')) if lf.endswith('.txt')]
        for chatlog in chatlogs:
            hits = []
            lines = open(chatlog, 'r', encoding='utf-16').readlines()
            for line in lines:
                if args.str_to_find in line:
                    hits.append(line)
            if hits:
                of.write('{}{}{}'.format(line_ending, chatlog, line_ending))
                for hit in hits:
                    of.write('{}{}'.format(hit.rstrip(), line_ending))
