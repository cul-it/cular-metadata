#!/usr/bin/env python3

# Generate json file manifest
# NOTE: This is a proof of concept; some hard-coded info for Africana ingest
# Input: fixity information (specify delimiter)
# Input: list of all assets to be included
# Output: json of manifest in template

import json
import datetime
import csv
import os
import copy
import re

# Hard coded stuff
DEPOSITOR = 'AFRICANA'
COLLECTION = 'ASRC_Lectures'
STEWARD = 'ea18'
HASH_LIST = { 'AFR-dig1-renamed.csv' : ',',
              'AFR-dig1-md-md5.txt' : ' ',
              'AFR-dig2-renamed.csv' : ',',
              'AFR-dig2-md-sha1.txt' : ' '}
ALLFILES = ['digpres1_completelist.txt', 'digpres2_completelist.txt']
FILENAMING_REGEX = re.compile('AFR_(\d{7})_V(\d{4})(.*)\.(mov|mp4|xml)')


def main():

    # Import template
    with open('manifest_template.json') as json_tmpl_src:
        json_tmpl = json.load(json_tmpl_src)

        # NOTE: Hardcoding stuff ahead... gotta figure out a better way to do this later
        # Pop some values
        json_tmpl[DEPOSITOR] = json_tmpl.pop('Depositor')
        json_tmpl[DEPOSITOR][COLLECTION] = json_tmpl[DEPOSITOR].pop('Collection Name')

        # Plop some values
        json_tmpl[DEPOSITOR][COLLECTION]['steward'] = STEWARD
        json_tmpl[DEPOSITOR][COLLECTION]['date_ingest'] = datetime.datetime.now().isoformat()
        json_tmpl[DEPOSITOR][COLLECTION]['date_update'] = datetime.datetime.now().isoformat()

        # Grab the template for the items
        json_item_tmpl = json_tmpl[DEPOSITOR][COLLECTION]['items']

    # Set up lookup for hash values for assets
    # possible values: md5, sha1, size
    # only required value: filename
    hashvalues = {}
    for hl in HASH_LIST.keys():
        with open(hl) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=HASH_LIST[hl])
            for row in reader:
                newvalue = os.path.normpath(row['filename'])
                hashvalues[newvalue] = {}
                if 'md5' in row:
                    hashvalues[newvalue]['md5'] = row['md5']
                if 'sha1' in row:
                    hashvalues[newvalue]['sha1'] = row['sha1']
                if 'size' in row:
                    hashvalues[newvalue]['size'] = row['size']

    # Go through all items
    itemlist = []
    for af in ALLFILES:
        with open(af, 'rU') as afli:
            allfilelist = afli.readlines()
            for afl in allfilelist:
                afl = os.path.normpath(afl).strip()
                dirname = os.path.dirname(afl)
                filename = os.path.basename(afl)

                # Ignore some files
                if filename == '.DS_Store':
                    continue
                elif filename == 'SFS_CopyCheck.txt':
                    continue
                elif filename.endswith('_audit.txt'):
                    continue
                elif filename.endswith('Spotlight'):
                    continue
                elif filename.endswith('.csv'):
                    continue
                elif filename.endswith('.log'):
                    continue
                elif filename.endswith('.xlsx'):
                    continue
                else:
                    newitem = copy.deepcopy(json_item_tmpl)
                    newitem[dirname] = newitem.pop('folder_work_level')
                    newitem[dirname][filename] = newitem[dirname].pop('file_asset_level')

                    # Get known parts
                    filenameparts = FILENAMING_REGEX.match(filename)
                    newitem[dirname][filename]['bib_id'] = filenameparts.group(1)
                    newitem[dirname][filename]['video_number'] = filenameparts.group(2)

                    # Logic for the rest of the parts
                    part = re.compile('_(\d{2})_').match(filenameparts.group(3))
                    if part is not None:
                        newitem[dirname][filename]['part_number'] = part.group(1)
                    else:
                        newitem[dirname][filename]['part_number'] = ''

                    # Now pull a hash value if we have it
                    if afl in hashvalues:
                        if 'sha1' in hashvalues[afl]:
                            newitem[dirname][filename]['sha1'] = hashvalues[afl]['sha1']
                        if 'md5' in hashvalues[afl]:
                            newitem[dirname][filename]['md5'] = hashvalues[afl]['md5']
                        if 'size' in hashvalues[afl]:
                            newitem[dirname][filename]['size'] = hashvalues[afl]['size']

                    # All's good
                    itemlist.append(newitem)
                    del(newitem)

    json_tmpl[DEPOSITOR][COLLECTION]['items'] = itemlist
    json_tmpl[DEPOSITOR][COLLECTION]['number_files'] = len(itemlist)
    print(json.dumps(json_tmpl, indent=4, separators=(',', ': ')))

if __name__ == "__main__":
    main()
