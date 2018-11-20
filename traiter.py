#!/usr/bin/env python3

"""Given a CSV file of natural history notes, parse traits."""

import re
import sys
import csv
import json
import argparse
import textwrap
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, Template
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

TEMPLATE = Template(
    '{{ left }}<span class="found">{{ middle }}</span>{{ right }}')


def parse_csv_file(args):
    """Build all of the parsers."""
    parsers = [(trait, parser(args)) for (trait, parser) in TRAITS
               if trait in args.traits]

    writer = None
    totals = {'rows': 0, 'empty': 0}

    reader = csv.DictReader(args.infile)
    for (i, in_row) in enumerate(reader, 1):
        totals['rows'] += 1

        if not i % 1000:
            print(i)

        if writer is None:
            # Setup the output file
            columns = reader.fieldnames
            preferred_columns = [p.preferred_value for (t, p) in parsers
                                 if p.preferred_value
                                 and p.preferred_value in columns]
            input_columns = (args.columns + preferred_columns
                             + args.extra_columns)
            parsed_columns = [f'parsed_{t}' for (t, p) in parsers]

            for col in parsed_columns:
                totals[col] = 0

            all_columns = parsed_columns + input_columns
            writer = output_start(args, all_columns)

        strings = [in_row[col] for col in args.columns]

        if not sum(len(s) for s in strings):
            totals['empty'] += 1
            continue

        out_row = {c: in_row[c] for c in input_columns}

        for trait, parser in parsers:
            preferred_value = ''
            if parser.preferred_value:
                preferred_value = in_row.get(parser.preferred_value, '')

            parsed = parser.parser(strings, preferred_value)

            column = f'parsed_{trait}'
            out_row[column] = output_cell(args, parsed, out_row)
            totals[column] += int(parsed['found'])

        output_row(args, writer, out_row)

    output_end(args, writer, preferred_columns, totals)


def output_start(args, all_columns):
    """Output the report header."""
    # Handle HTML output
    if args.html:
        return []

    # Handle CSV output
    writer = csv.DictWriter(args.outfile, fieldnames=all_columns)
    writer.writeheader()
    return writer


def output_row(args, writer, out_row):
    """Output a report row."""
    # Handle HTML output
    if args.html:
        writer.append(out_row)
        return

    # Handle CSV output
    writer.writerow(out_row)


def output_cell(args, parsed, row):
    """Output a report cell."""
    # Handle CSV output
    if not args.html:
        return json.dumps(parsed)

    # Handle HTML output
    if parsed['found']:
        field_name = parsed['field']
        field = row[field_name]
        start = parsed['start']
        end = parsed['end']
        left = field[:start] if start else ''
        middle = field[start:end]
        right = field[end:] if end <= len(field) else ''
        row[field_name] = TEMPLATE.render(
            left=left, middle=middle, right=right)
    return parsed


def output_end(args, writer, preferred_columns, totals):
    """Output the report footer."""
    # Handle CSV output
    if not args.html:
        return

    # Handle HTML output
    env = Environment(loader=FileSystemLoader('./templates'))
    template = env.get_template('traiter.html')
    report = template.render(
        args=vars(args),
        now=datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M'),
        rows=writer,
        preferred_columns=preferred_columns,
        totals=totals)
    args.outfile.write(report)


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
                        help="""A comma separated list of any extra columns to
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
