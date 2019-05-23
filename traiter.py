#!/usr/bin/env python3

"""Given a CSV file of natural history notes, parse traits."""

import sys
import argparse
import textwrap
from traiter.all_traits import TRAITS
from traiter.file_parser import FileParser
from traiter.readers.csv_reader import CsvReader
from traiter.writers.csv_writer import CsvWriter
from traiter.writers.html_writer import HtmlWriter


__VERSION__ = '0.4.0'


INPUT_FORMATS = {
    'csv': CsvReader}

OUTPUT_FORMATS = {
    'csv': CsvWriter,
    'html': HtmlWriter}


def parse_traits(args):
    """Parse the input."""
    trait_parsers = [(trait, trait_parser(args))
                     for trait, trait_parser in TRAITS.items()
                     if trait in args.trait]

    reader = INPUT_FORMATS[args.input_format](args)
    writer = OUTPUT_FORMATS[args.output_format](args)

    file_parser = FileParser(args, trait_parsers)

    with reader as input_file, writer as output_file:

        for i, record in enumerate(input_file, 1):

            if args.skip and i <= args.skip:
                continue

            record_parser = file_parser.new_record_parser()
            parsed_record = record_parser.parse_record(record)

            output_file.record(record, parsed_record)

            if args.stop and i >= args.stop:
                break


def parse_args():
    """Process command-line arguments."""
    description = """Extract traits from the file."""
    arg_parser = argparse.ArgumentParser(
        allow_abbrev=True,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(description))

    arg_parser.add_argument(
        '--version', '-V', action='version',
        version='%(prog)s v{}'.format(__VERSION__))

    arg_parser.add_argument(
        '--input-file', '-i', type=argparse.FileType('r'), default=sys.stdin,
        help='''The input file containing the traits. Defaults to stdin.''')

    arg_parser.add_argument(
        '--output-file', '-o', type=argparse.FileType('w'), default=sys.stdout,
        help='''Output the results to this file. Defaults to stdout.''')

    arg_parser.add_argument(
        '--trait', '-t', required=True, action='append',
        choices=TRAITS.keys(),
        help="""A trait to extract.""")

    arg_parser.add_argument(
        '--search-field', '-s', action='append', metavar='FIELD',
        help=f"""A field that contains traits. You may use this argument more
            than once.""")

    arg_parser.add_argument(
        '--extra-field', '-e', action='append', metavar='FIELD',
        help="""An extra field to to append to an output row. You may use this
            argument more than once.""")

    arg_parser.add_argument(
        '--as-is', '-a', action='append', metavar='FIELD:TRAIT', default=[],
        help="""A FIELD:TRAIT to use as is. For example:
            --as-is='age:life_stage' will use the value in the record's "age"
            field, if there is one, as a parsed value of "life_stage". You may
            use this argument more than once and you may need to quote it.""")

    arg_parser.add_argument(
        '--input-format', '-I', default='csv', choices=INPUT_FORMATS.keys(),
        help="""The data input format. The default is "csv".""")

    arg_parser.add_argument(
        '--output-format', '-O', default='csv', choices=OUTPUT_FORMATS.keys(),
        help="""Output the result in this format. The default is "csv".""")

    arg_parser.add_argument(
        '--skip', type=int,
        help="""Skip this many records at the beginning of the input file.""")

    arg_parser.add_argument(
        '--stop', type=int,
        help="""Stop after this many records are processed.""")

    arg_parser.add_argument(
        '--log-every', type=int, metavar='N',
        help="""Log after message after processing every N input records.""")

    args = arg_parser.parse_args()

    as_is = {x.split(':')[1].strip(): [] for x in args.as_is}
    for arg in args.as_is:
        key, val = arg.split(':')
        as_is[val.strip()].append(key.strip())
    args.as_is = as_is

    return args


if __name__ == "__main__":
    ARGS = parse_args()
    parse_traits(ARGS)
