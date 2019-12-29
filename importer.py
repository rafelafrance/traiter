#!/usr/bin/env python3

"""Import data from the given format and put it into a database."""

import sys
import argparse
from pylib.shared import util
# from pylib.shared import temp_dir
from pylib.shared.readers import csv_reader


INPUT_FORMATS = {
    'csv': csv_reader}


def parse_args():
    """Process command-line arguments."""
    parser = argparse.ArgumentParser(
        allow_abbrev=True,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        fromfile_prefix_chars='@',
        description=util.shorten("""Import raw data for extracting traits."""))

    parser.add_argument(
        '--version', '-V', action='version',
        version='%(prog)s v{}'.format(util.__VERSION__))

    parser.add_argument(
        '--column', '-c', action='append',
        help="""A column that contains data. You should use this argument once
            for every column you want from the input file.""")

    parser.add_argument(
        '--all-columns', '-a', action='store_true',
        help="""This indicates that you want to import all columns from the
            input file.""")

    parser.add_argument(
        '--db', '-d', required=True,
        help="""The path to the database file to import the data into.""")

    parser.add_argument(
        '--input-file', '-i', type=argparse.FileType('r'), default=sys.stdin,
        help="""The file containing the raw data. Defaults to STDIN.""")

    parser.add_argument(
        '--input-format', '-I', default='csv',
        choices=INPUT_FORMATS.keys(),
        help="""The file format. The default is "csv".""")

    # parser.add_argument(
    #     '-t', '--temp-dir', metavar='DIR',
    #     help="""Place temporary files in this directory. All files will be
    #         deleted after aTRAM completes. The directory must exist.""")
    #
    # parser.add_argument(
    #     '--keep-temp-dir', action='store_true',
    #     help="""This flag will keep the temporary files in the --temp-dir
    #     around for debugging.""")

    args = parser.parse_args()

    # temp_dir.exists(args.temp_dir)

    return args


if __name__ == "__main__":
    ARGS = parse_args()
    INPUT_FORMATS[ARGS.input_format].read(ARGS)
