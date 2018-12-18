"""
Filter csv files and keep the hits
"""
import sys
import argparse as ap
import glob as g

# pylint: disable=invalid-name
# pylint: disable=line-too-long

def arg_parse():
    """
    Parse the command line arguments
    """
    p = ap.ArgumentParser()
    p.add_argument('column_name',
                   type=str,
                   help='column_name to search')
    p.add_argument('operation',
                   choices=['gt', 'lt', 'eq'])
    p.add_argument('limit',
                   type=float,
                   help='limit to search by')
    return p.parse_args()

if __name__ == "__main__":
    args = arg_parse()
    templist = sorted(g.glob('*.csv'))
    nfiles = len(templist)
    hits = []
    for i, t in enumerate(templist):
        print('Processing file {} of {}...'.format(i+1, nfiles))
        with open(t, 'r') as infile:
            # read in the entire file including the header
            total = infile.readlines()
            # headers need tidying to remove first space after ,
            header = total[0].split(',')
            for i in range(0, len(header)):
                header[i] = " ".join(header[i].split())
            # locate the column we want
            try:
                column_id = header.index(args.column_name)
            except ValueError:
                print("Column {} not found!".format(args.column_name))
                sys.exit(1)
            # send the body on for searching
            lines = total[1:]

        for line in lines:
            # check we have a number to compare, otherwise skip line
            try:
                check = float(line.split(',')[column_id])
            except TypeError:
                continue
            # check the number vs the limit
            if args.operation == 'gt' and check > args.limit:
                hits.append("{},{}".format(t, line))
            elif args.operation == 'eq' and check == args.limit:
                hits.append("{},{}".format(t, line))
            elif args.operation == 'lt' and check < args.limit:
                hits.append("{},{}".format(t, line))
            else:
                pass

    # save the hits
    with open('results.txt', 'w') as outfile:
        for hit in hits:
            outfile.write('{}'.format(hit))
