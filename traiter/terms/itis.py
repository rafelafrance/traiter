"""Get terms from an SQLite ITIS database."""

import csv
import sqlite3
from pathlib import Path
from typing import Optional, Union

from .csv_ import Csv
from ..const import DATA_DIR

# This points to a database (or a sym link) in the client's data directory
ITIS_DB = DATA_DIR / 'ITIS.sqlite'


class Itis(Csv):
    """A dictionary of temp."""

    ###########################################################################
    # Other constructors related to the ITIS database

    @classmethod
    def itis(
            cls,
            taxon: str,
            label: Optional[str] = None,
            kingdom_id: int = 5,
            rank_id: int = 220,
            attr: str = 'lower'
    ) -> 'Itis':
        """Get temp from the ITIS database.

        name       = the ITIS term's hypernym, this is often a family name
        kingdom_id = 5 == Animalia
        rank_id    = 220 == Species
        attr       = the spacy attribute to match on
        """
        terms = []

        label = label if label else taxon

        tsn = """ select tsn from taxonomic_units where unit_name1 = ?; """
        names = """
            select complete_name
              from hierarchy
              join taxonomic_units using (tsn)
             where hierarchy_string like ?
               and kingdom_id = ?
               and rank_id = ?;
               """

        with sqlite3.connect(ITIS_DB) as cxn:
            cursor = cxn.execute(tsn, (taxon,))
            tsn = cursor.fetchone()[0]
            mask = f'%-{tsn}-%'
            taxa = {n[0] for n in cxn.execute(names, (mask, kingdom_id, rank_id))}

        terms += [{'label': label, 'pattern': t, 'attr': attr, 'pos': 'PROPN'}
                  for t in sorted(taxa)]
        return cls(terms=terms)

    @classmethod
    def taxon_level_terms(
            cls,
            other: 'Csv',
            label: str,
            new_label: str = '',
            level: str = 'species',
            attr='lower'
    ) -> 'Itis':
        """Get species or genus names only: 'Canis lupus' -> 'lupus'."""
        idx = 1 if level == 'species' else 0
        new_label = new_label if new_label else level
        return cls.pick_words(other, label, idx=idx, new_label=new_label, attr=attr)

    @classmethod
    def abbrev_species(
            cls, other: 'Csv', label: str, attr: str = 'lower'
    ) -> 'Itis':
        """Get abbreviated species: 'Canis lupus' -> 'C. lupus'."""
        return cls.abbrev_terms(other, label=label, attr=attr)

    @classmethod
    def itis_common_names(
            cls,
            taxon: str,
            kingdom_id: int = 5,
            rank_id: int = 220,
            replace: bool = False
    ) -> 'Itis':
        """Guides often use common names instead of scientific name.

        kingdom_id =   5 == Animalia
        rank_id    = 220 == Species
        """
        terms = []

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

        for common, sci_name in names.items():
            term = {
                'label': 'common_name',
                'pattern': common,
                'attr': 'lower',
                'pos': 'PROPN',
            }
            if replace:
                term['replace'] = sci_name
            terms.append(term)

        return cls(terms=terms)

    @classmethod
    def mock_itis_traits(cls, mock_terms_csv: Union[str, Path], taxon: str) -> 'Itis':
        """Set up mock traits for testing with Travis.

        The ITIS database is too big to put into GitHub so we use a mock database
        for testing.
        """
        # Bypass using this in tests for now.
        print('Could not find ITIS database.')

        taxon = taxon.lower()

        with open(mock_terms_csv) as term_file:
            reader = csv.DictReader(term_file)
            terms = list(reader)

        for term in terms:
            label = term['label']
            term['label'] = label if label else taxon

        return cls(terms=terms)
