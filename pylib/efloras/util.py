"""Holds misc functions and constants."""

import csv
from pathlib import Path
from datetime import datetime
import regex
from pylib.shared.util import FLAGS
from pylib.efloras.shared_patterns import CATALOG


RAW_DIR = Path('.') / 'data' / 'raw'

EFLORAS_NA_FAMILIES = RAW_DIR / 'eFlora_family_list.csv'


def camel_to_snake(name):
    """Convert a camel case string to snake case."""
    split = regex.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return regex.sub('([a-z0-9])([A-Z])', r'\1_\2', split).lower()


def get_families():
    """Get a list of all families in the eFloras North American catalog."""
    families = {}

    with open(EFLORAS_NA_FAMILIES) as in_file:

        for family in csv.DictReader(in_file):

            times = {'created': '', 'modified': '', 'count': 0}

            path = RAW_DIR / family['Name']
            if path.exists():
                times['count'] = len(list(path.glob('**/*.html')))
                if times['count']:
                    stat = path.stat()
                    times['created'] = datetime.fromtimestamp(
                        stat.st_ctime).strftime('%Y-%m-%d %H:%M')
                    times['modified'] = datetime.fromtimestamp(
                        stat.st_mtime).strftime('%Y-%m-%d %H:%M')

            families[family['Name'].lower()] = {
                'name': family['Name'],
                'taxon_id': family['Taxon Id'],
                'lower_taxa': family['# Lower Taxa'],
                'volume': family['Volume'],
                'created': times['created'],
                'modified': times['modified'],
                'count': times['count'],
                }

    return families


def print_families(families):
    """Display a list of all families."""
    template = '{:<20} {:>10}  {:<25}  {:<20}  {:<20} {:>10}'

    print(template.format(
        'Family',
        'Taxon Id',
        'Volume',
        'Directory Created',
        'Directory Modified',
        'File Count'))

    for family in families.values():
        print(template.format(
            family['name'],
            family['taxon_id'],
            family['volume'],
            family['created'],
            family['modified'],
            family['count'] if family['count'] else ''))


def split_keywords(value):
    """Convert a vocabulary string into separate words."""
    return regex.split(fr"""
        \s* \b (?: {CATALOG['conj'].pattern} | {CATALOG['prep'].pattern} )
            \b \s* [,]? \s*
        | \s* [,\[\]] \s*
        """, value, flags=FLAGS)


def part_phrase(catalog, leaf_part):
    """Build a grouper rule for the leaf part."""
    return catalog.grouper(f'{leaf_part}_phrase', f"""
            ( location ( word | punct | prep )* )?
            (?P<part> {leaf_part} )
            """)
