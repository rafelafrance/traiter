#!/usr/bin/env python3

"""Given a CSV file of natural history notes, parse traits."""

import re
import csv
import argparse
import textwrap
from lib.trait_parsers.body_mass import ParseBodyMass
from lib.trait_parsers.life_stage import ParseLifeStage
from lib.trait_parsers.sex import ParseSex
from lib.trait_parsers.total_length import ParseTotalLength
from lib.trait_parsers.testes_state import ParseTestesState

__VERSION__ = '0.3.0'


DEFAULT_COLS = 'dynamicproperties, occurrenceremarks, fieldnotes'

TRAITS = [
    ('body_mass', ParseBodyMass),
    ('life_stage', ParseLifeStage),
    ('sex', ParseSex),
    ('total_length', ParseTotalLength),
    ('testes_state', ParseTestesState)]
TRAIT_NAMES = ', '.join([i[0] for i in TRAITS])


def parse_csv_file(args):
    """Build all of the parsers."""
    columns = re.split(r'\s*,\s*', args.columns)
    parsers = [parser() for (trait, parser) in TRAITS
               if trait in args.traits]
    parsers = [(parser.parser, parser.preferred) for parser in parsers]

    with open(args.csv, 'r') as in_file:
        reader = csv.DictReader(in_file)
        for row in reader:
            strings = [row[col] for col in columns]
            print(reader.line_num)
            for parser, preferred in parsers:
                print(parser(strings, row.get(preferred, '')))


def parse_args():
    """Process command-line arguments."""
    description = """Extract traits from the given CSV file's columns."""
    parser = argparse.ArgumentParser(
        allow_abbrev=True,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(description))

    parser.add_argument('--version', action='version',
                        version='%(prog)s {}'.format(__VERSION__))

    parser.add_argument('--columns', '-c', default=DEFAULT_COLS,
                        help=f"""A comma separated list of columns that contain
                            traits. The default is: '{DEFAULT_COLS}'.""")

    parser.add_argument('--traits', '-t', default=TRAIT_NAMES,
                        help=f"""A comma separated list of the traits to
                            extract. The default is to select them all. The
                            options are: '{TRAIT_NAMES}'.""")

    parser.add_argument('csv',
                        help='''The CSV file containing the traits.''')

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    ARGS = parse_args()
    parse_csv_file(ARGS)
