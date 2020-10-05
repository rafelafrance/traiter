"""Get terms from various sources (CSV files or SQLite database."""

import csv
import sqlite3
from pathlib import Path
from typing import Dict, List

from hyphenate import hyphenate_word

from traiter.pylib.util import DATA_DIR

ITIS_DB = DATA_DIR / 'ITIS.sqlite'
VOCAB_DIR = Path.cwd() / 'src' / 'vocabulary'

TermsListType = List[Dict[str, str]]


def read_terms(term_path):
    """Read and cache the terms."""
    with open(term_path) as term_file:
        reader = csv.DictReader(term_file)
        return list(reader)


def itis_terms(
        name: str,
        kingdom_id: int = 5,
        rank_id: int = 220,
        abbrev: bool = False,
        species: bool = False
) -> TermsListType:
    """Get terms from the ITIS database.

    kingdom_id =   5 == Animalia
    rank_id    = 220 == Species
    """
    # Bypass using this in tests for now.
    if not ITIS_DB.exists():
        print('Could not find ITIS database.')
        return mock_itis_traits(name)

    select_tsn = """ select tsn from taxonomic_units where unit_name1 = ?; """
    select_names = """
        select complete_name
          from hierarchy
          join taxonomic_units using (tsn)
         where hierarchy_string like ?
           and kingdom_id = ?
           and rank_id = ?;
           """

    with sqlite3.connect(ITIS_DB) as cxn:
        cursor = cxn.execute(select_tsn, (name,))
        tsn = cursor.fetchone()[0]
        mask = f'%-{tsn}-%'
        taxa = {n[0].lower() for n in
                cxn.execute(select_names, (mask, kingdom_id, rank_id))}

    terms = []
    name = name.lower()
    for taxon in sorted(taxa):
        terms.append({
            'label': name,
            'pattern': taxon,
            'attr': 'lower',
            'replace': taxon,
        })
        if abbrev:
            words = taxon.split()
            if len(words) > 1:
                first, *rest = words
                first = first[0]
                rest = ' '.join(rest)
                terms.append({
                    'label': name,
                    'pattern': f'{first} . {rest}',
                    'attr': 'lower',
                    'replace': taxon,
                })
        if species:
            words = taxon.split()
            if len(words) > 1:
                genus, species, *rest = words
                terms.append({
                    'label': 'species',
                    'pattern': species,
                    'attr': 'lower',
                    'replace': species.lower(),
                })

    return terms


def hyphenate_terms(terms: TermsListType) -> TermsListType:
    """Systematically handle hyphenated terms."""
    new_terms = []
    for term in terms:

        if term['hyphenate']:
            parts = term['hyphenate'].split('-')
        else:
            parts = hyphenate_word(term['pattern'])

        for i in range(1, len(parts)):
            replace = term['replace']
            hyphenated = ''.join(parts[:i]) + '-' + ''.join(parts[i:])
            new_terms.append({
                'label': term['label'],
                'pattern': hyphenated,
                'attr': term['attr'],
                'replace': replace if replace else term['pattern'],
                'category': term['category'],
            })
            hyphenated = ''.join(parts[:i]) + '\xad' + ''.join(parts[i:])
            new_terms.append({
                'label': term['label'],
                'pattern': hyphenated,
                'attr': term['attr'],
                'replace': replace if replace else term['pattern'],
                'category': term['category'],
            })

    return new_terms


def get_common_names(
        name: str, kingdom_id: int = 5, rank_id: int = 220) -> TermsListType:
    """Guides often use common names instead of scientific name.

        kingdom_id =   5 == Animalia
        rank_id    = 220 == Species
    """
    if not ITIS_DB.exists():
        return []

    select_tsn = """ select tsn from taxonomic_units where unit_name1 = ?; """
    select_names = """
    select vernacular_name, complete_name
      from vernaculars
      join taxonomic_units using (tsn)
      join hierarchy using (tsn)
     where hierarchy_string like ?
       and kingdom_id = ?
       and rank_id = ?;
        """

    with sqlite3.connect(ITIS_DB) as cxn:
        cursor = cxn.execute(select_tsn, (name,))
        tsn = cursor.fetchone()[0]
        mask = f'%-{tsn}-%'
        names = {n[0].lower(): n[1] for n in
                 cxn.execute(select_names, (mask, kingdom_id, rank_id))}

    terms = []
    for common, sci_name in names.items():
        terms.append({
            'label': 'common_name',
            'pattern': common,
            'attr': 'lower',
            'replace': sci_name,
        })

    return terms


def mock_itis_traits(name: str) -> TermsListType:
    """Set up mock traits for testing with Travis."""
    name = name.lower()
    terms = []

    mock_path = VOCAB_DIR / 'mock_itis_terms.csv'
    if mock_path.exists():
        terms = read_terms(mock_path)
        for term in terms:
            label = term['label']
            term['label'] = label if label else name

    return terms
