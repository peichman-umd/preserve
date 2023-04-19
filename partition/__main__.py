#!/usr/bin/env python3

from .classes import FileSet
from .exceptions import ConfigError, DuplicateFileError, ClobberingFileError
from preserve.utils import header
import argparse
import os
import shutil
import sys

PARTITIONING_PATTERN = r"^([a-z]+?)-(\d+?)[-_][^.]+?\.\S+?$"


def parse_args():
    ''' Parse command line arguments '''

    parser = argparse.ArgumentParser(
        description='Partition a tree of files based on various schemes'
        )

    parser.add_argument(
        'source',
        help='Root directory to be partitioned',
        action='store'
        )

    parser.add_argument(
        'destination',
        help='Output directory (if exists, must be empty)',
        action='store'
        )

    parser.add_argument(
        '-m', '--mode',
        choices=['copy', 'move', 'dryrun'],
        help='Dryrun, move, or copy files to destination',
        action='store',
        default='dryrun'
        )

    parser.add_argument(
        '-v', '--version',
        action='version',
        help='Print version number and exit',
        version='%(prog)s 0.1'
        )

    return parser.parse_args()


def check_args(args):
    ''' Validate the provided arguments '''

    if not os.path.isdir(args.source):
        raise ConfigError("Source directory not found")


def has_duplicates(mapping):
    all_dest = dict()
    for source, destination in mapping.items():
        all_dest.setdefault(destination, []).append(source)
    duplicates = [tuple(all_dest[d]) for d in all_dest if len(all_dest[d]) > 1]
    if duplicates:
        return duplicates
    else:
        return False


def main():

    try:
        sys.stderr.write(header("Partition Tool"))

        """ (1) Parse args """
        args = parse_args()

        """ (2) Validate the provided arguments """
        check_args(args)
        print(f"Running with the following arguments:")
        width = max([len(k) for k in args.__dict__])
        for k in args.__dict__:
            print(f"  {k:>{width}} : {getattr(args, k)}")

        """ (3) Create FileSet """
        fileset = FileSet.from_filesystem(args.source)
        print(f"\nAnalyzing files: {len(fileset)} files, " +
              f"{round(fileset.bytes/2**30, 2)} GiB")

        """ (4) Create partition map """
        print(f"Creating mapping to partitioned tree...")
        mapping = fileset.partition_by(PARTITIONING_PATTERN, args.destination)

        """ (5) Check for duplicate files """
        duplicates = has_duplicates(mapping)
        if duplicates:
            raise DuplicateFileError(f"Duplicate filenames detected: {duplicates}")
        else:
            print("Destination paths are all confirmed to be unique...")

        """ (6) Check for clobbering """
        existing_files = [filter(os.path.isfile, mapping.values())]
        if existing_files:
            joined_clobbered = '\n'.join(existing_files)
            raise ClobberingFileError(f"Files clobbered: {joined_clobbered}")

        """ (7) Move, copy, or print """
        print(f"Partitioning files ({args.mode} mode)...")
        for n, (source, destination) in enumerate(mapping.items(), 1):
            print(f"  {n}. {source} -> {destination}")
            if args.mode == 'dryrun':
                continue
            else:
                os.makedirs(os.path.dirname(destination), exist_ok=True)
                if args.mode == 'copy':
                    shutil.copyfile(source, destination)
                elif args.mode == 'move':
                    shutil.move(source, destination)

        """ (8) Summarize results """
        print("Partitioning complete.")

    except Exception as err:
        print(f"ERROR: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
