#!/usr/bin/env python3

import csv
import os
import json
import time
import re
from collections import defaultdict

# TODO: Fill in values
collection_name = 'MATH VIDEOS'
collection_id = '6789012'
numberfiles = 123456 # Does this include contents of _Documentation, as well?
steward = 'abc123'
createdate = time.strftime('%Y-%m-%d')
hashdeep_input = 'mathtest.txt' # Path/name of file with hashdeep manifest

# Create manifest of items
items = defaultdict(dict)

# NOTE: Regular expression to handle identifiers, connects to later part of script
idre = re.compile('MATH_(\d{1,7})_V(\d{1,4})')

# TODO: Accept file as input; for now, hardcode
with open(hashdeep_input) as csvfile:
    for i in range(5):
        if i==1:
            header=csvfile.readline().replace('%%%% ','').strip().split(',')
        csvfile.readline()
    reader = csv.DictReader(csvfile, fieldnames=header)
    for row in reader:
        filepath,filename = row['filename'].split('/')

        # Set up if doesn't already exist
        items[filepath] = items.get(filepath, {})
        items[filepath][filename] = items[filepath].get(filename, {})

        items[filepath][filename]['sha1'] = row['sha1']
        items[filepath][filename]['size'] = row['size']        

        # NOTE: Adjust script to parse out components of filename for identifiers
        components = idre.match(filename)
        bibid, videonum = components.group(1), components.group(2)
        items[filepath][filename]['bibid'] = bibid
        items[filepath][filename]['video_number'] = videonum

# Generate collection level JSON
collection = {}
collection[collection_name] = {}
collection[collection_name]['phys_coll_id'] = collection_id
collection[collection_name]['steward'] = steward
collection[collection_name]['timestamp'] = createdate
collection[collection_name]['items'] = items

# Print out
print(json.dumps(collection, indent=4))

