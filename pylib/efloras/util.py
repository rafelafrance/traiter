"""Holds misc functions and constants."""

import regex
import csv
from pathlib import Path
from datetime import datetime
from pylib.stacked_regex.rule import replacer
from pylib.efloras.shared_patterns import RULE


__VERSION__ = '0.1.0'


RAW_DIR = Path('.') / 'data' / 'raw'

EFLORAS_NA_FAMILIES = RAW_DIR / 'eFlora_family_list.csv'

FLAGS = regex.VERBOSE | regex.IGNORECASE


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
    """Convert a keyword string into separate keywords."""
    return regex.split(fr"""
        \s* \b (?: {RULE['conj'].pattern} | {RULE['prep'].pattern} ) 
            \b \s* [,]? \s* 
        | \s* [,\[\]] \s*
        """, value, flags=FLAGS)


def set_size_values(trait, token):
    """Update the size measurements with normalized values."""
    units, multiplier = {}, {}

    if token.groups.get('high_length_upper'):
        token.groups['high_length'] = token.groups['high_length_upper']

    if token.groups.get('units_length_upper'):
        token.groups['units_length'] = token.groups['units_length_upper']

    units['length'] = token.groups.get('units_length', '').lower()
    units['width'] = token.groups.get('units_width', '').lower()

    # No units means it's not a measurement
    if not (units['length'] or units['width']):
        return False

    if not units['length']:
        multiplier['width'] = 10.0 if units['width'] == 'cm' else 1.0
        multiplier['length'] = multiplier['width']
    elif not units['width']:
        multiplier['length'] = 10.0 if units['length'] == 'cm' else 1.0
        multiplier['width'] = multiplier['length']
    else:
        multiplier['length'] = 10.0 if units['length'] == 'cm' else 1.0
        multiplier['width'] = 10.0 if units['width'] == 'cm' else 1.0

    for dimension in ['length', 'width']:
        for value in ['min', 'low', 'high', 'max']:
            key = f'{value}_{dimension}'
            if key in token.groups:
                setattr(trait, key,
                        float(token.groups[key]) * multiplier[dimension])
    return True


def part_phrase(leaf_part):
    """Build a replacer rule for the leaf part."""
    return replacer(f'{leaf_part}_phrase', f"""
        ( location ( word | punct )* )?
        (?P<part> {leaf_part} )
        """)
