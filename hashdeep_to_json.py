#!/usr/bin/env python3

import csv
import os
import json
import time
import re
import sys
import configparser
import argparse
from collections import defaultdict, OrderedDict

def collectionvalues(collsection):
    collection = {}
    collection_name = collsection['collection_name']
    if collsection['phys_coll_id'] == '':
        collheader = (('steward', collsection['steward']),
                      ('number_files', 0))
    else:
         collheader = (('phys_coll_id', collsection['phys_coll_id']),
                      ('steward', collsection['steward']),
                      ('number_files', 0))
    collection[collection_name] = OrderedDict(collheader)
    return collection


def locationvalues(locsection):
    locations = {}
    storage = locsection['storage']

    locations[storage] = {}
    locations[storage]['date_ingest'] = time.strftime('%Y-%m-%d')
#    locations[storage]['date_update'] = None # TODO for update procedure

    return locations


def itemlisting(fixitysection):
    fixity_input = fixitysection['fixity']
    items = defaultdict(dict)
    numberfiles = 0

    idre = re.compile(fixitysection['regex'])

    with open(fixity_input, 'rU') as csvfile:
        if fixitysection['hashdeep'] == '1':
            csvfile = csvfile.read().splitlines()
            headers = csvfile[1].replace('%%%% ', '')
            csvfile = csvfile[5:]
            csvfile.insert(0, headers)
            reader = csv.DictReader(csvfile)
        else:
            reader = csv.DictReader(csvfile)

        for row in reader:
            numberfiles = numberfiles + 1
            # This assumes a two directory structure
            filepath,filename = row['filename'].split('/')

            # Set up if doesn't already exist
            items[filepath] = items.get(filepath, {})
            items[filepath][filename] = items[filepath].get(filename, {})

            filevalues = row.keys()
            for fv in filevalues:
                if fv != 'filename':
                    if row[fv] != '':
                        items[filepath][filename][fv] = row[fv]

            components = idre.match(filename)

            if components is not None:
                bibid = components.group(1)
                items[filepath][filename]['bibid'] = bibid

            else:
                sys.exit("Error parsing regular expression for {}".format(row['filename']))

    return items, numberfiles


def verifyexisting(updateconfig, updatejsonname):
    # Do we have an existing JSON?
    if not os.path.isfile(updatejsonname):
        sys.exit("Unable to find existing JSON: {0}".format(updatejsonname))
    else:
        with open(updatejsonname, 'r') as em:
            manifest = json.load(em)

    # Test: Same collection?
    # Filename should already force a mismatch, but just in case.
    existingcollname = updateconfig['COLLECTION']['collection_name']
    if next(iter(manifest)) != existingcollname:
        sys.exit("Collection name mismatch.")

    existingphyscolid = updateconfig['COLLECTION']['phys_coll_id']
    if manifest[existingcollname]['phys_coll_id'] != existingcollid:
        sys.exit("Physical collection ID mismatch.")




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('configfile', metavar='[config_file]',
                        help='path to configuration file with values for JSON manifest')
    parser.add_argument('-u', '--update', action='store_true', help='flag to indicate update')
    args = parser.parse_args()

    if not os.path.isfile(args.configfile):
        sys.exit('Config file not found. Quitting.')

    config = configparser.ConfigParser()
    config.read(args.configfile)

    # Generate Output from Depositor/Collection pair
    thiscollection = collectionvalues(config['COLLECTION'])
    collname = next(iter(thiscollection))

    jsonfilename = collname.replace('/', '_')
    jsonfilename = jsonfilename.replace(' ', '_') # Just in case
    jsonfilename = "_EM_{0}.json".format(jsonfilename,)

    if not args.update:
        thiscollection[collname]['locations'] = locationvalues(config['LOCATIONS'])
        thiscollection[collname]['items'],count = itemlisting(config['ITEMS'])
        thiscollection[collname]['number_files'] = count
    else:
        thiscollection = verifyexisting(config, jsonfilename)

        sys.exit("be done right now")

    if os.path.isfile(jsonfilename):
        sys.exit("File already exists, will not overwrite.")
    else:
        with open(jsonfilename, 'w') as output:
            output.write(json.dumps(thiscollection, indent=4))

if __name__ == "__main__":
    main()
