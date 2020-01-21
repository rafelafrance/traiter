#!/usr/bin/env python3

"""Parse extracted traiter_efloras web pages."""

import sys
import argparse
import textwrap
from traiter_shared.util import __VERSION__
import traiter_efloras.util as util
import traiter_efloras.trait_groups as tg
from traiter_efloras.writers import html_writer
from traiter_efloras.writers import csv_writer
from traiter_efloras.readers.efloras_reader import efloras_reader


INPUT_FORMATS = {
    'traiter_efloras': efloras_reader}

OUTPUT_FORMATS = {
    'csv': csv_writer,
    'html': html_writer}


def parse_traits(args, families):
    """Perform actions based on the arguments."""
    if args.list_families:
        util.print_families(families)
        sys.exit()

    if args.list_traits:
        for trait in tg.TRAIT_NAMES:
            print(trait)
        sys.exit()

    df = INPUT_FORMATS[args.input_format](args, families)
    OUTPUT_FORMATS[args.output_format](args, families, df)


def parse_args(families):
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
        '--family', '-f', action='append',
        help="""Which family to extract.""")

    arg_parser.add_argument(
        '--trait', '-t', default='',
        help="""The traits to extract.""")

    arg_parser.add_argument(
        '--input-format', '-I', default='traiter_efloras',
        choices=INPUT_FORMATS.keys(),
        help="""The data input format. The default is "traiter_efloras".""")

    arg_parser.add_argument(
        '--output-file', '-o', type=argparse.FileType('w'), default=sys.stdout,
        help="""Output the results to this file. Defaults to stdout.""")

    arg_parser.add_argument(
        '--output-format', '-O', default='csv', choices=OUTPUT_FORMATS.keys(),
        help="""Output the result in this format. The default is "csv".""")

    arg_parser.add_argument(
        '--list-families', '-F', action='store_true',
        help="""List families available to extract and exit.""")

    arg_parser.add_argument(
        '--list-traits', '-T', action='store_true',
        help="""List traits available to extract and exit.""")

    args = arg_parser.parse_args()

    if args.family:
        args.family = [x.lower() for x in args.family]
        for family in args.family:
            if family not in families:
                sys.exit(f'"{family}" has not been downloaded')

    return args


if __name__ == '__main__':
    FAMILIES = {k: v for k, v in util.get_families().items() if v['count']}
    ARGS = parse_args(FAMILIES)
    parse_traits(ARGS, FAMILIES)
