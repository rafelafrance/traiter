#!/usr/bin/env python3

"""Given a CSV file of natural history notes, parse traits."""

import re
import sys
import argparse
import textwrap
from lib.readers.csv_reader import CsvReader
from lib.writers.csv_writer import CsvWriter
from lib.writers.html_writer import HtmlWriter
from lib.parsers.sex import Sex
from lib.parsers.body_mass import BodyMass
from lib.parsers.life_stage import LifeStage
from lib.parsers.total_length import TotalLength
from lib.parsers.testes_state import TestesState
# from lib.parsers.testes_size import TestesSize

__VERSION__ = '0.4.0'


DEFAULT_COLS = 'dynamicproperties, occurrenceremarks, fieldnotes'

INPUT_FORMATS = {
    'csv': CsvReader,
}
INPUT_OPTIONS = [k for k, v in INPUT_FORMATS.items()]

OUTPUT_FORMATS = {
    'csv': CsvWriter,
    'html': HtmlWriter,
}
OUTPUT_OPTIONS = [k for k, v in OUTPUT_FORMATS.items()]

# These are ordered
TRAITS = [
    ('sex', Sex),
    ('body_mass', BodyMass),
    ('life_stage', LifeStage),
    ('total_length', TotalLength),
    ('testes_state', TestesState),
    #   ('testes_size', ParseTestesSize)],
]
TRAIT_OPTIONS = ', '.join([i[0] for i in TRAITS])


def parse_traits(args):
    """Parse the input."""
    reader = INPUT_FORMATS[args.input_format](args)
    writer = OUTPUT_FORMATS[args.output_format](args)

    parsers = [(trait, parser()) for (trait, parser) in TRAITS
               if trait in args.traits]

    writer.start()

    with reader as infile:
        for i, row in enumerate(infile, 1):

            if args.skip and i <= args.skip:
                continue

            for trait, parser in parsers:
                results = parser.parse(row)
                writer.cell(trait, results)

            writer.row()

            if args.stop and i >= args.stop:
                break

    writer.end()


def parse_args():
    """Process command-line arguments."""
    description = """Extract traits from the given CSV file's columns."""
    parser = argparse.ArgumentParser(
        allow_abbrev=True,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(description))

    parser.add_argument('--version', action='version',
                        version='%(prog)s {}'.format(__VERSION__))

    parser.add_argument('--traits', '-t', default=TRAIT_OPTIONS,
                        help=f"""A comma separated list of the traits to
                            extract. The default is to select them all. You may
                            want to quote this argument. The options are:
                            '{TRAIT_OPTIONS}'.""")

    parser.add_argument('--csv-columns', '-c', default=DEFAULT_COLS,
                        help=f"""A comma separated ordered list of columns that
                            contain traits. The traits will be searched in the
                            given order. You may need to quote this argument.
                            The default is: '{DEFAULT_COLS}'.""")

    parser.add_argument('--csv-extra-columns', '-e', default='',
                        help="""A comma separated list of any extra columns to
                            append to an output row. You may need to quote this
                            argument.""")

    parser.add_argument('--input-format', '-i', default='csv',
                        choices=INPUT_OPTIONS,
                        help="""The data input format.
                            The default is "csv".""")

    parser.add_argument('--output-format', '-o', default='csv',
                        choices=OUTPUT_OPTIONS,
                        help="""Output the result in this format.
                            The default is "csv".""")

    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin,
                        help='''The input file containing the traits.
                            Defaults to stdin.''')

    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout,
                        help='''Output the results to this file.
                            Defaults to stdout.''')

    parser.add_argument('--skip', type=int,
                        help="""Skip this many records at the beginning of the
                            input file.""")

    parser.add_argument('--stop', type=int,
                        help="""Stop after this many records are processed.""")

    args = parser.parse_args()

    args.traits = re.split(r'\s*,\s*', args.traits)
    args.csv_columns = re.split(r'\s*,\s*', args.csv_columns)
    args.csv_extra_columns = [
        c for c in re.split(r'\s*,\s*', args.csv_extra_columns) if c]

    return args


if __name__ == "__main__":
    ARGS = parse_args()
    parse_traits(ARGS)
