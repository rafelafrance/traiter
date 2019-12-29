#!/usr/bin/env python3

"""Build traits from the raw input."""

import argparse
from pylib.shared import util
from pylib.shared import db


def parse_traits(args):
    """Build traits from the raw input."""
    with db.connect(args.db) as cxn:
        for row in db.select_raw(cxn, args.limit, args.offset):
            print(row['raw_id'])
            # for trait in traits
            #   for input field in input fields


def parse_args() -> argparse.Namespace:
    """Process command-line arguments."""
    parser = argparse.ArgumentParser(
        allow_abbrev=True,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        fromfile_prefix_chars='@',
        description=util.shorten("""Import raw data for extracting traits."""))

    parser.add_argument(
        '--db', '-d', required=True,
        help="""The path to the database file to import the data into.""")

    parser.add_argument(
        '--no-early-stopping', action='store_true',
        help="""Continue parsing traits after there is a match on an input
            field.""")

    parser.add_argument(
        '--limit', type=int, default=0,
        help="""Stop after this many records are processed.""")

    parser.add_argument(
        '--offset', type=int, default=0,
        help="""Skip this many records at the beginning of the input.""")

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    ARGS = parse_args()
    parse_traits(ARGS)
