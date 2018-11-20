#!/usr/bin/env python3

"""Given a CSV file of natural history notes, parse traits."""

import re
import sys
import csv
import json
import argparse
import textwrap
from jinja2 import Environment, FileSystemLoader
from lib.trait_parsers.sex import ParseSex
from lib.trait_parsers.body_mass import ParseBodyMass
from lib.trait_parsers.life_stage import ParseLifeStage
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
    parsers = [(trait, parser(args)) for (trait, parser) in TRAITS
               if trait in args.traits]

    writer = None

    reader = csv.DictReader(args.infile)
    for (i, in_row) in enumerate(reader, 1):

        if not i % 1000:
            print(i)

        if writer is None:
            # Setup the output file
            input_fields = get_input_fields(args, parsers, reader)
            parsed_fields = [f'parsed_{t}' for (t, p) in parsers]
            writer = output_header(args, input_fields, parsed_fields)

        strings = [in_row[col] for col in args.columns]
        out_row = {c: in_row[c] for c in input_fields}

        for trait, parser in parsers:
            column = f'parsed_{trait}'

            preferred_value = ''
            if parser.preferred_value:
                preferred_value = in_row.get(parser.preferred_value, '')

            parsed = parser.parser(strings, preferred_value)

            out_row[column] = json.dumps(parsed)

        output_row(args, writer, out_row)

    output_footer(args, writer)


def get_input_fields(args, parsers, reader):
    """Get field names (w/out traits) from the arguments & input file."""
    fieldnames = args.extra_columns + args.columns
    columns = reader.fieldnames
    fieldnames += [p.preferred_value for (t, p) in parsers
                   if p.preferred_value and p.preferred_value in columns]
    return fieldnames


def output_header(args, input_fields, parsed_fields):
    """Output the report header."""
    if args.html:
        return []

    writer = csv.DictWriter(
        args.outfile, fieldnames=(input_fields + parsed_fields))
    writer.writeheader()
    return writer


def output_row(args, writer, out_row):
    """Output a report row."""
    if args.html:
        return

    writer.writerow(out_row)


def output_footer(args, writer):
    """Output the report footer."""
    if not args.html:
        return


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
                        help=f"""A comma separated ordered list of columns that
                            contain traits. The traits will be searched in the
                            given order. You may need to quote this argument.
                            The default is: '{DEFAULT_COLS}'.""")

    parser.add_argument('--traits', '-t', default=TRAIT_NAMES,
                        help=f"""A comma separated list of the traits to
                            extract. The default is to select them all. You may
                            want to quote this argument. The options are:
                            '{TRAIT_NAMES}'.""")

    parser.add_argument('--extra-columns', '-e', default='',
                        help="""A comma separated list of any extra fields to
                            append to an output row. You may need to quote this
                            argument.""")

    parser.add_argument('--html', action='store_true',
                        help="""Output the result as an HTML table.""")

    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin,
                        help='''The input file containing the traits.''')

    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout,
                        help='''Output the results to this file.''')

    args = parser.parse_args()

    args.traits = re.split(r'\s*,\s*', args.traits)
    args.columns = re.split(r'\s*,\s*', args.columns)
    args.extra_columns = [
        c for c in re.split(r'\s*,\s*', args.extra_columns) if c]

    return args


if __name__ == "__main__":
    ARGS = parse_args()
    parse_csv_file(ARGS)
