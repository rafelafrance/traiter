#!/usr/bin/env python3

"""Given a CSV file of natural history notes, parse traits."""

import sys
import argparse
import textwrap
from lib.file_parser import FileParser
from lib.readers.csv_reader import CsvReader
from lib.writers.csv_writer import CsvWriter
from lib.writers.html_writer import HtmlWriter
from lib.traits.sex import Sex
from lib.traits.body_mass import BodyMass
from lib.traits.life_stage import LifeStage
from lib.traits.ear_length import EarLength
from lib.traits.tail_length import TailLength
from lib.traits.testes_size import TestesSize
from lib.traits.testes_state import TestesState
from lib.traits.total_length import TotalLength
from lib.traits.hind_foot_length import HindFootLength

__VERSION__ = '0.3.0'


INPUT_FORMATS = {
    'csv': CsvReader,
}
INPUT_OPTIONS = [k for k, v in INPUT_FORMATS.items()]

OUTPUT_FORMATS = {
    'csv': CsvWriter,
    'html': HtmlWriter,
}
OUTPUT_OPTIONS = [k for k, v in OUTPUT_FORMATS.items()]

TRAITS = [
    ('sex', Sex),
    ('body_mass', BodyMass),
    ('life_stage', LifeStage),
    ('total_length', TotalLength),
    ('tail_length', TailLength),
    ('hind_foot_length', HindFootLength),
    ('ear_length', EarLength),
    ('testes_size', TestesSize),
    ('testes_state', TestesState),
]
TRAIT_OPTIONS = [t[0] for t in TRAITS]


def parse_traits(args):
    """Parse the input."""
    parsers = [(trait, parser(args)) for (trait, parser) in TRAITS
               if trait in args.trait]

    reader = INPUT_FORMATS[args.input_format](args)
    writer = OUTPUT_FORMATS[args.output_format](args)

    parsed_file = FileParser(args, parsers)

    with reader as infile, writer as outfile:

        for i, record in enumerate(infile, 1):

            if args.skip and i <= args.skip:
                continue

            parser = parsed_file.new_record_parser()
            parsed_record = parser.parse_record(record)

            outfile.record(record, parsed_record)

            if args.stop and i >= args.stop:
                break


def parse_args():
    """Process command-line arguments."""
    description = """Extract traits from the file."""
    parser = argparse.ArgumentParser(
        allow_abbrev=True,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(description))

    parser.add_argument(
        '--version', '-V', action='version',
        version='%(prog)s v{}'.format(__VERSION__))

    parser.add_argument(
        '--trait', '-t', required=True, action='append', choices=TRAIT_OPTIONS,
        help="""A trait to extract.""")

    parser.add_argument(
        '--search-field', '-s', action='append', metavar='FIELD',
        help=f"""A field that contains traits. You may use this argument more
            than once.""")

    parser.add_argument(
        '--extra-field', '-e', action='append', metavar='FIELD',
        help="""An extra field to to append to an output row. You may use this
            argument more than once.""")

    parser.add_argument(
        '--as-is', '-a', action='append', metavar='FIELD:TRAIT', default=[],
        help="""A FIELD:TRAIT to use as is. For example:
            --as-is='age:life_stage' will use the value in the record's "age"
            field, if there is one, as a parsed value of "life_stage". You may
            use this argument more than once and you may need to quote it.""")

    parser.add_argument(
        '--input-format', '-i', default='csv', choices=INPUT_OPTIONS,
        help="""The data input format. The default is "csv".""")

    parser.add_argument(
        '--output-format', '-o', default='csv', choices=OUTPUT_OPTIONS,
        help="""Output the result in this format. The default is "csv".""")

    parser.add_argument(
        '--skip', type=int,
        help="""Skip this many records at the beginning of the input file.""")

    parser.add_argument(
        '--stop', type=int,
        help="""Stop after this many records are processed.""")

    parser.add_argument(
        'infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
        help='''The input file containing the traits. Defaults to stdin.''')

    parser.add_argument(
        'outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout,
        help='''Output the results to this file. Defaults to stdout.''')

    args = parser.parse_args()

    as_is = {x.split(':')[1].strip(): [] for x in args.as_is}
    for arg in args.as_is:
        key, val = arg.split(':')
        as_is[val.strip()].append(key.strip())
    args.as_is = as_is

    return args


if __name__ == "__main__":
    ARGS = parse_args()
    parse_traits(ARGS)
