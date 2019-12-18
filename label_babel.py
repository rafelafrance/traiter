#!/usr/bin/env python3

"""Parse labels extracted from herbarium specimens."""


import sys
import argparse
import textwrap
from pylib.shared.util import __VERSION__
from pylib.shared.importers import csv_reader

"""
Date, taxon names, collector, collector number
admin units: like state, county, country
scientificName for the binomial and genus and species separately
"""

INPUT_FORMATS = {
    'csv': csv_reader}

OUTPUT_FORMATS = {}


def parse_traits(args):
    """Perform actions based on the arguments."""
    reader = INPUT_FORMATS[args.input_format]
    reader.read(args)


def parse_args():
    """Process command-line arguments."""
    description = """Download data from the eFloras website."""
    arg_parser = argparse.ArgumentParser(
        allow_abbrev=True,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(description),
        fromfile_prefix_chars='@')

    arg_parser.add_argument(
        '--version', '-V', action='version',
        version='%(prog)s v{}'.format(__VERSION__))

    arg_parser.add_argument(
        '--trait', '-t', default='',
        help="""The traits to extract.""")

    arg_parser.add_argument(
        '--search-field', '-s', action='append', metavar='FIELD',
        help=f"""A field that contains the data to parse. You may use this
            argument more than once.""")

    arg_parser.add_argument(
        '--extra-field', '-e', action='append', metavar='FIELD',
        help="""An extra field to to append to an output row. You may use this
            argument more than once.""")

    arg_parser.add_argument(
        '--input-file', '-i', type=argparse.FileType('r'), default=sys.stdin,
        help="""The input file containing the raw data. Defaults to stdin.""")

    arg_parser.add_argument(
        '--input-format', '-I', default='csv',
        choices=INPUT_FORMATS.keys(),
        help="""The data input format. The default is "csv".""")

    arg_parser.add_argument(
        '--output-file', '-o', type=argparse.FileType('w'), default=sys.stdout,
        help="""Output the results to this file. Defaults to stdout.""")

    arg_parser.add_argument(
        '--output-format', '-O', default='csv', choices=OUTPUT_FORMATS.keys(),
        help="""Output the result in this format. The default is "csv".""")

    args = arg_parser.parse_args()

    return args


if __name__ == "__main__":
    ARGS = parse_args()
    parse_traits(ARGS)
