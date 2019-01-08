#!/usr/bin/env python3

from pathlib import Path
from collections import defaultdict
import sys

RMCPREFIX = 'RM*' # FIND AND REPLACE OKGO

##### ASSETS SECTION #################
af = {}
assetdir = Path('.')
ac = defaultdict(lambda: 0)
for adir in assetdir.glob('RM*'):
    for fl in adir.glob('RM*'):
        bl = fl.name
        af[bl] = [fl]
        ext = fl.suffix.lstrip('.')
        ac[ext] = ac[ext] + 1



##### FIXITY SECTION #################
startdir = Path('./_Fixity')
if startdir.is_dir():
    # Get ext/count from FileCount.txt
    fc = {}
    fcs = startdir / 'FileCount.txt'
    fcs = open(fcs).readlines()
    for line in fcs:
        line = line.strip().split()
        fc[line[1]] = int(line[0])

    # Find the rest of the fixity files; assume sidecars start with RM*
    for l in list(startdir.glob('RM*')):
        bn = l.name.replace('.md5' , '')
        hv = open(l).read().strip()
        af[bn].append(hv)
else:
    sys.exit('Re-run the script in asset directory.')

# Verify actual file count against reported file count
# Exit on the two error conditions
if sorted(fc) == sorted(ac):
    for f in fc:
        if fc[f] != ac[f]:
            sys.exit("Count mismatch on {0}".format(f))
else:
    # Depending on how often this goes wrong,
    # fill in more debugging help.
    sys.exit("Extension mismatch.")


###### MANIFEST SECTION ################
# Generate the manifest
print('filename,md5')
for a in af:
    print(','.join([af[a][0].as_posix(), af[a][1]]))
