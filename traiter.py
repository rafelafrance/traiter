#!/usr/bin/env python3

"""Given a CSV file of natural history notes, parse traits."""

import re
import sys
import argparse
import textwrap
from lib.readers.csv_reader import CsvReader
from lib.writers.csv_writer import CsvWriter
from lib.writers.html_writer import HtmlWriter
from lib.parsers.any_value import AnyValue
from lib.parsers.sex import Sex
from lib.parsers.body_mass import BodyMass
from lib.parsers.life_stage import LifeStage
# from lib.parsers.ear_length import EarLength
# from lib.parsers.tail_length import TailLength
# from lib.parsers.testes_size import TestesSize
from lib.parsers.testes_state import TestesState
from lib.parsers.total_length import TotalLength
# from lib.parsers.hind_foot_length import HindFootLength

__VERSION__ = '0.3.0'


DEFAULT_COLS = 'dynamicproperties,occurrenceremarks,fieldnotes'

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
    #   ('ear_length', EarLength)],
    #   ('testes_size', TestesSize)],
    #   ('tail_length', TailLength)],
    #   ('hind_foot_length', HindFootLength)],
]
TRAIT_OPTIONS = ', '.join([i[0] for i in TRAITS])


def parse_traits(args):
    """Parse the input."""
    any_value = AnyValue(args)

    parsers = [(trait, parser(args)) for (trait, parser) in TRAITS
               if trait in args.traits]

    reader = INPUT_FORMATS[args.input_format](args)
    writer = OUTPUT_FORMATS[args.output_format](args)

    with reader as infile, writer as outfile:
        for i, row in enumerate(infile, 1):

            if args.skip and i <= args.skip:
                continue

            for trait, parser in parsers:

                # Check for a value in the preferred field
                field = args.preferred_fields.get(trait)
                value = row.get(field, '')
                results = any_value.extended_parse(
                    value, f'preferred_{trait}', field)

                # No value in the preferred field so parse the data
                if not results:
                    for field in args.search_fields:
                        results.extend(
                            parser.extended_parse(row[field], trait, field))

                outfile.cell(results)

            outfile.row()

            if args.stop and i >= args.stop:
                break


def parse_args():
    """Process command-line arguments."""
    description = """Extract traits from the file."""
    parser = argparse.ArgumentParser(
        allow_abbrev=True,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(description))

    parser.add_argument('--version', '-V', action='version',
                        version='%(prog)s v{}'.format(__VERSION__))

    parser.add_argument(
        '--traits', '-t', default=TRAIT_OPTIONS,
        help=f"""A comma separated list of the traits to extract. The default
            is to select them all. You may want to quote this argument. The
            traits will be searched in the given order. The options are:
            '{TRAIT_OPTIONS}'.""")

    parser.add_argument(
        '--search_fields', '-f', default=DEFAULT_COLS, metavar='COLUMNS',
        help=f"""A comma separated ordered list of fields that contain traits.
            You may need to quote this argument. The default is:
            '{DEFAULT_COLS}'.""")

    parser.add_argument(
        '--extra-fields', '-e', default='', metavar='COLUMNS',
        help="""A comma separated list of any extra fields to append to an
            output row. You may need to quote this argument.""")

    parser.add_argument(
        '--preferred-fields', '-p', default='', metavar='COLUMNS',
        help="""A comma separated list of trait=field to use, if filled,
            instead of parsing the --search-fields. For example:
            --preferred-fields='body_mass=mass, life_stage=age' will use the
            value in the row's "mass" field, if there is one, instead of
            parsing the body_mass for any of the --search_fields.  Likewise for
            life_stage and "age". You may need to quote this argument.""")

    parser.add_argument(
        '--input-format', '-i', default='csv', choices=INPUT_OPTIONS,
        help="""The data input format. The default is "csv".""")

    parser.add_argument(
        '--output-format', '-o', default='csv', choices=OUTPUT_OPTIONS,
        help="""Output the result in this format. The default is "csv".""")

    parser.add_argument(
        'infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
        help='''The input file containing the traits. Defaults to stdin.''')

    parser.add_argument(
        'outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout,
        help='''Output the results to this file. Defaults to stdout.''')

    parser.add_argument('--skip', type=int,
                        help="""Skip this many records at the beginning of the
                            input file.""")

    parser.add_argument('--stop', type=int,
                        help="""Stop after this many records are processed.""")

    args = parser.parse_args()

    args.traits = re.split(r'\s*,\s*', args.traits)
    args.search_fields = re.split(r'\s*,\s*', args.search_fields)
    args.extra_fields = [
        col for col in re.split(r'\s*,\s*', args.extra_fields) if col]

    prefs = [item for pair in re.split(r'\s*,\s*', args.preferred_fields)
             for item in re.split(r'\s*=\s*', pair)]
    args.preferred_fields = dict(zip(prefs[::2], prefs[1::2]))

    return args


if __name__ == "__main__":
    ARGS = parse_args()
    parse_traits(ARGS)
