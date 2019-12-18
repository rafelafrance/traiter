#!/usr/bin/env python

"""Build and run a wget command."""

import os
import sys
import time
import random
import argparse
import textwrap
import urllib.request
import regex
from lxml import html
from pylib.shared.util import __VERSION__
from . import util


LINK = regex.compile(
    r'.*florataxon\.aspx\?flora_id=1&taxon_id=(?P<taxon_id>\d+)',
    regex.VERBOSE | regex.IGNORECASE)


def efloras(family_name, taxon_id, parents):
    """Get a family of taxa from the efloras web site."""
    parents.add(taxon_id)

    path = util.RAW_DIR / family_name / f'taxon_id_{taxon_id}.html'
    url = ('http://www.efloras.org/florataxon.aspx?flora_id=1'
           f'&taxon_id={taxon_id}')

    print(f'Downloading: {url}')

    if not path.exists():
        urllib.request.urlretrieve(url, path)
        time.sleep(random.randint(10, 20))  # 15 sec +/- 5 sec

    with open(path) as in_file:
        page = html.fromstring(in_file.read())

    for link in page.xpath('//a'):
        href = link.attrib.get('href', '')
        match = LINK.match(href)
        if match and match.group('taxon_id') not in parents:
            efloras(family_name, match.group('taxon_id'), parents)


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
        '--family', '-f', action='append',
        help="""Which family to download.""")

    arg_parser.add_argument(
        '--list-families', '-l', action='store_true',
        help="""Print a list of families available for download.""")

    args = arg_parser.parse_args()

    if args.family:
        args.family = [x.lower() for x in args.family]
        for family in args.family:
            if family not in FAMILIES:
                sys.exit(f'"{family}" is not available.')

    return args


def main(args, families):
    """Perform actions based on the arguments."""
    if args.list_families:
        util.print_families(families)
        sys.exit()

    for family in args.family:
        family_name = FAMILIES[family]['name']
        taxon_id = FAMILIES[family]['taxon_id']
        os.makedirs(util.RAW_DIR / family_name, exist_ok=True)
        efloras(family_name, taxon_id, set())


if __name__ == "__main__":
    FAMILIES = util.get_families()
    ARGS = parse_args()
    main(ARGS, FAMILIES)
