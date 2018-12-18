"""
Filter csv files and keep the hits
"""
import argparse as ap
import glob as g

# pylint: disable=invalid-name
# pylint: disable=line-too-long

def arg_parse():
    """
    Parse the command line arguments
    """
    p = ap.ArgumentParser()
    p.add_argument('column_id',
                   type=int,
                   help='column id to search')
    p.add_argument('operation',
                   choices=['gt', 'lt', 'eq'])
    p.add_argument('limit',
                   type=str,
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
            lines = infile.readlines()[1:]

        if args.operation == 'gt':
            hits += ["{},{}".format(t, line) for line in lines if line.split(',')[args.column_id - 1] > args.limit]
        elif args.operation == 'eq':
            hits += ["{},{}".format(t, line) for line in lines if line.split(',')[args.column_id - 1] == args.limit]
        else:
            hits += ["{},{}".format(t, line) for line in lines if line.split(',')[args.column_id - 1] < args.limit]

    # save the hits
    with open('results.txt', 'w') as outfile:
        for hit in hits:
            outfile.write('{}'.format(hit))
