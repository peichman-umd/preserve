import csv
import os
import re
import sys
from .manifest import Manifest

#=== SUBCOMMAND =============================================================
#         NAME: compare
#  DESCRIPTION: check for the presence of files in inventories of various
#               formats (TSM backup, file analyzer, this script)
#============================================================================

def compare(args):
    '''Compare asset manifests checking for the presence of assets only'''
    asset_sets = {}
    all_paths = [args.first] + args.other 
    for path in all_paths:
        if not os.path.exists(path):
            sys.exit("{0} does not exist".format(path))
        else:
            m = Manifest(path)
            asset_sets[path] = set(
                [(os.path.relpath(a.path, m.root), a.bytes) for a in m]
                )
            print(asset_sets)

    # Report degree to which the inventories all match
    common = set.intersection(*asset_sets.values())
    print("{} values are common to all the supplied files:".format(
                                                                len(common)))

    # Report the differences (if any) in the individual files
    for n, (path, asset_set) in enumerate(asset_sets.items()):
        unique = asset_set.difference(common)
        print(" => Path {0}: {1} values are unique to {2}".format(
                n+1, len(unique), path))
        if unique is not None:
            sorted_files = sorted(unique)
            for n, (relpath, bytes) in enumerate(sorted_files):
                print("     ({0}) {1} -- {2} bytes".format(n+1, relpath, bytes))
    print('')

