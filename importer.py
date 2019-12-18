#!/usr/bin/env python3

"""Import data."""

import sys
import argparse
from pylib.shared.util import __VERSION__, shorten
from pylib.shared.readers import csv_reader


INPUT_FORMATS = {
    'csv': csv_reader}


def parse_args():
    """Process command-line arguments."""
    arg_parser = argparse.ArgumentParser(
        allow_abbrev=True,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        fromfile_prefix_chars='@',
        description=shorten("""
        """))

    arg_parser.add_argument(
        '--version', '-V', action='version',
        version='%(prog)s v{}'.format(__VERSION__))

    arg_parser.add_argument(
        '--column', '-c', action='append',
        help="""A column that contains data. You should use this argument once
            for every column you want from the input file.""")

    arg_parser.add_argument(
        '--all-columns', '-a', action='store_true',
        help="""This indicates that you want to import all columns from the
            input file.""")

    arg_parser.add_argument(
        '--db', '-d', required=True,
        help="""The path to the database file to import the data into.""")

    arg_parser.add_argument(
        '--input-file', '-i', type=argparse.FileType('r'), default=sys.stdin,
        help="""The file containing the raw data. Defaults to STDIN.""")

    arg_parser.add_argument(
        '--input-format', '-I', default='csv',
        choices=INPUT_FORMATS.keys(),
        help="""The file format. The default is "csv".""")

    args = arg_parser.parse_args()

    return args


if __name__ == "__main__":
    ARGS = parse_args()
    INPUT_FORMATS[ARGS.input_format].read(ARGS)
