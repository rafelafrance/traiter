"""Get terms from various sources like CSV files or an SQLite database."""

import csv
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Union

from hyphenate import hyphenate_word

from traiter.pylib.util import DATA_DIR
import traiter.vocabulary as vocab

ITIS_DB = DATA_DIR / 'ITIS.sqlite'
VOCAB_DIR = Path.cwd() / 'src' / 'vocabulary'

TermsList = List[Dict[str, str]]


def shared_terms(csv_file: str) -> TermsList:
    """Get the path to a shared vocabulary file."""
    return read_terms(Path(vocab.__file__).parent / csv_file)


def read_terms(term_path: Union[str, Path]) -> TermsList:
    """Read and cache the terms from a CSV file.

    The CSV file must contain the columns:
        label = the term's hypernym, 'color' is a hypernym of 'blue'
        pattern = the term itself
        attr = the spaCy attribute being matched upon, this is typically
            'lower' but sometimes 'regex' is used.
    """
    with open(term_path) as term_file:
        reader = csv.DictReader(term_file)
        return list(reader)


def itis_terms(
        taxon: str,
        label: Optional[str] = None,
        kingdom_id: int = 5,
        rank_id: int = 220,
        attr: str = 'lower'
) -> TermsList:
    """Get terms from the ITIS database.

    name       = the ITIS term's hypernym, this is often a family name
    kingdom_id = 5 == Animalia
    rank_id    = 220 == Species
    attr       = the spacy attribute to match on
    """
    label = label if label else taxon

    # Bypass using this in tests for now.
    if not ITIS_DB.exists():
        print('Could not find ITIS database.')
        return mock_itis_traits(taxon)

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
        cursor = cxn.execute(select_tsn, (taxon,))
        tsn = cursor.fetchone()[0]
        mask = f'%-{tsn}-%'
        taxa = {n[0] for n in cxn.execute(select_names, (mask, kingdom_id, rank_id))}

    terms = [{'label': label, 'pattern': t, 'attr': attr} for t in sorted(taxa)]
    return terms


def taxon_level_terms(
        terms: TermsList,
        label: str,
        new_label: str = '',
        level: str = 'species',
        attr='lower'
) -> TermsList:
    """Get species or genus names only: 'Canis lupus' -> 'lupus'."""
    new_terms = []
    idx = 1 if level == 'species' else 0
    new_label = new_label if new_label else level
    used_patterns = set()
    for term in terms:
        if term['label'] == label:
            words = term['pattern'].split()
            if len(words) > 1 and words[0][-1] != '.':
                pattern = words[idx]
                if pattern not in used_patterns:
                    new_terms.append({
                        'label': new_label, 'pattern': pattern, 'attr': attr})
                used_patterns.add(pattern)
    return new_terms


def abbrev_species(terms: TermsList, label: str, attr='lower') -> TermsList:
    """Get abbreviated species: 'Canis lupus' -> 'C. lupus'."""
    new_terms = []
    for term in terms:
        if term['label'] == label:
            full_name = term['pattern']
            first, *rest = full_name.split()
            if rest and first[-1] != '.':
                rest = ' '.join(rest)
                new_terms.append({
                    'label': label,
                    'pattern': f'{first[0]}. {rest}',
                    'attr': attr,
                    'replace': full_name})
    return new_terms


def hyphenate_terms(terms: TermsList) -> TermsList:
    """Systematically handle hyphenated terms.

    We cannot depend on terms being present in a contiguous form. We need a
    systematic method for handling hyphenated terms. The hyphenate library is
    great for this but sometimes we need to handle non-standard hyphenations
    manually. Non-standard hyphenations are stored in the terms CSV file.
    """
    new_terms = []
    for term in terms:

        if term['hyphenate']:
            # Handle a non-standard hyphenation
            parts = term['hyphenate'].split('-')
        else:
            # A standard hyphenation
            parts = hyphenate_word(term['pattern'])

        for i in range(1, len(parts)):
            replace = term['replace']
            for hyphen in ('-', '\xad'):
                hyphenated = ''.join(parts[:i]) + hyphen + ''.join(parts[i:])
                new_terms.append({
                    'label': term['label'],
                    'pattern': hyphenated,
                    'attr': term['attr'],
                    'replace': replace if replace else term['pattern'],
                    'category': term['category']})

    return new_terms


def itis_common_names(
        taxon: str, kingdom_id: int = 5, rank_id: int = 220, replace: bool = False
) -> TermsList:
    """Guides often use common names instead of scientific name.

    kingdom_id =   5 == Animalia
    rank_id    = 220 == Species
    """
    if not ITIS_DB.exists():
        print('Could not find ITIS database.')
        return mock_itis_traits(taxon)

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
        cursor = cxn.execute(select_tsn, (taxon,))
        tsn = cursor.fetchone()[0]
        mask = f'%-{tsn}-%'
        names = {
            n[0].lower(): n[1]
            for n in cxn.execute(select_names, (mask, kingdom_id, rank_id))
        }

    terms = []
    for common, sci_name in names.items():
        term = {'label': 'common_name', 'pattern': common, 'attr': 'lower'}
        if replace:
            term['replace'] = sci_name
        terms.append(term)

    return terms


def mock_itis_traits(name: str) -> TermsList:
    """Set up mock traits for testing with Travis.

    The ITIS database is too big to put into GitHub so we use a mock database
    for testing.
    """
    name = name.lower()
    terms = []

    mock_path = VOCAB_DIR / 'mock_itis_terms.csv'
    if mock_path.exists():
        terms = read_terms(mock_path)
        for term in terms:
            label = term['label']
            term['label'] = label if label else name

    return terms
