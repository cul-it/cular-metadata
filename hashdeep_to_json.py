#!/usr/bin/env python3

# but the general idea is generally there
# rules:
# Mention every single file
# EVery single file has to have an ID
# Ask MAP and EF whether that's one field or two (bibid and itemid or identifier?)
# TODO: consistent input, which might mean massaging hashdeep or hashmyfiles output
#filename,size,md5,sha1



from collections import defaultdict
import argparse
import csv
import datetime
import os
import sys
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', metavar='[input_file]',
                        type=argparse.FileType('r'),
                        help='input fixity file')
    parser.add_argument('depcoll', metavar='[depositor_collection]')
    parser.add_argument('physcollid', metavar='[collection_id]',
                        help='physical collection ID')
    parser.add_argument('steward', metavar='[steward]')
    args = parser.parse_args()

    hashlist = defaultdict(tuple)
    dirs = set()
    files = set()

    # Column headings we should/might have:
    # filename
    # size
    # sha1
    # optionally a flag for whether the BIBID is in the filename or not

    reader = csv.DictReader(args.inputfile)
    for row in reader:
        hashlist[row['filename']] = (row['size'], row['md5'], row['sha1'])
        # figure out a more elegant solution to this later
        dirs.add(os.path.split(row['filename'])[0])
        files.add(os.path.split(row['filename'])[1])

    items = {}
    for d in dirs:
        items[d] = {}
        for f in files:
            if len(hashlist['{0}/{1}'.format(d,f)]) != 0:
                thissize = hashlist['{0}/{1}'.format(d,f)][0]
                thismd5 = hashlist['{0}/{1}'.format(d,f)][1]
                thissha1 = hashlist['{0}/{1}'.format(d,f)][2]
                items[d][f] = {'size': thissize, 'md5': thismd5, 'sha1': thissha1 } 
            
    em = {args.depcoll: {'phys_coll_id': args.physcollid,
                         'steward': args.steward,
                         'items': items}}

    sdepcoll = args.depcoll.replace('/', '_')
    jsonfilename = '_EM_{0}.json'.format(sdepcoll)

    with open(jsonfilename, 'w') as output:
        output.write(json.dumps(em, indent=4))

if __name__ == "__main__":
    main()
