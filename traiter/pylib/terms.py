"""Get terms from various sources like CSV files or an SQLite database.

The CSV file must contain the columns:
    label = the term's hypernym, 'color' is a hypernym of 'blue'
    pattern = the term itself
    attr = the spaCy attribute being matched upon, this is typically
        'lower' but sometimes 'regex' or 'text' is used. The default is 'lower'.
"""

import csv
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Union

from hyphenate import hyphenate_word

import traiter.vocabulary as vocab
from traiter.pylib.util import DATA_DIR

# This points to a database (or a sym link) in the client's data directory
ITIS_DB = DATA_DIR / 'ITIS.sqlite'

# This points to the client's directory
VOCAB_DIR = Path.cwd() / 'src' / 'vocabulary'

# This points to the traiter vocabulary files
SHARED_CSV = Path(vocab.__file__).parent.glob('*.csv')

PathList = Union[str, Path, List[str], List[Path]]
StrList = Union[str, List[str]]


class Terms:
    """A dictionary of terms."""

    def __init__(
            self,
            csv_file: Optional[PathList] = None,
            shared: Optional[StrList] = None,
            pattern_dicts: Optional[StrList] = None
    ) -> None:
        self.terms = []
        self.patterns = {}

        if csv_file:
            self.read_csv(csv_file)

        if shared:
            self.shared(shared)

        if pattern_dicts:
            self.pattern_dicts(pattern_dicts)

    def __iter__(self):
        yield from self.terms

    def __getattr__(self, name: str) -> Dict:
        return self.patterns.get(name, {})

    def pattern_dicts(self, columns: StrList) -> None:
        """Create a dict from a column in the terms."""
        columns = columns if isinstance(columns, list) else columns.split()
        for column in columns:
            self.patterns[column] = {t['pattern']: v for t in self.terms
                                     if (v := t.get(column)) not in (None, '')}

    def shared(self, shared: StrList, labels: Optional[StrList] = None) -> None:
        """Get the path to a shared vocabulary file.
            shared: Names (possibly abbreviated) of the the shared files to include.
            label:  A list of labels to include from the files. None = all
        """
        paths = shared.split() if isinstance(shared, str) else shared

        paths = {c for c in SHARED_CSV
                 if any(c.name.lower().startswith(p) for p in paths)}

        self.read_csv(list(paths), labels)

    def read_csv(self, csv_file: PathList, labels: Optional[StrList] = None) -> None:
        """Read and cache the terms from a CSV file.

            csv_file: A file name or a list of files.
            label:    A list of labels to include from the files. None = all
        """
        labels = labels.split() if isinstance(labels, str) else labels

        for path in self._paths(csv_file):
            with open(path) as term_file:
                reader = csv.DictReader(term_file)
                terms = list(reader)

            if labels:
                terms = [t for t in terms if t['label'] in labels]

            for term in terms:
                if not term.get('attr'):
                    term['attr'] = 'lower'

            self.terms += terms

    @staticmethod
    def _paths(path_list: PathList) -> List[Union[str, Path]]:
        """Convert the path list into a list of paths."""
        if isinstance(path_list, Path):
            return [path_list]
        elif isinstance(path_list, str):
            return path_list.split()
        return path_list

    def itis(
            self,
            taxon: str,
            label: Optional[str] = None,
            kingdom_id: int = 5,
            rank_id: int = 220,
            attr: str = 'lower'
    ) -> None:
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
            self.mock_itis_traits(taxon)
            return

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

        self.terms += [{'label': label, 'pattern': t, 'attr': attr, 'pos': 'PROPN'}
                       for t in sorted(taxa)]

    def taxon_level_terms(
            self,
            label: str,
            new_label: str = '',
            level: str = 'species',
            attr='lower'
    ) -> None:
        """Get species or genus names only: 'Canis lupus' -> 'lupus'."""
        idx = 1 if level == 'species' else 0
        new_label = new_label if new_label else level
        used_patterns = set()
        for term in self.terms:
            if term['label'] == label:
                words = term['pattern'].split()
                if len(words) > 1 and words[0][-1] != '.':
                    pattern = words[idx]
                    if pattern not in used_patterns:
                        self.terms.append({
                            'label': new_label,
                            'pattern': pattern,
                            'attr': attr,
                            'pos': 'PROPN',
                        })
                    used_patterns.add(pattern)

    def abbrev_species(self, label: str, attr='lower') -> None:
        """Get abbreviated species: 'Canis lupus' -> 'C. lupus'."""
        for term in self.terms:
            if term['label'] == label:
                full_name = term['pattern']
                first, *rest = full_name.split()
                if rest and first[-1] != '.':
                    rest = ' '.join(rest)
                    self.terms.append({
                        'label': label,
                        'pattern': f'{first[0]}. {rest}',
                        'attr': attr,
                        'replace': full_name,
                        'pos': 'PROPN',
                    })

    def hyphenate_terms(self) -> None:
        """Systematically handle hyphenated terms.

        We cannot depend on terms being present in a contiguous form. We need a
        systematic method for handling hyphenated terms. The hyphenate library is
        great for this but sometimes we need to handle non-standard hyphenations
        manually. Non-standard hyphenations are stored in the terms CSV file.
        """
        for term in self.terms:

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
                    self.terms.append({
                        'label': term['label'],
                        'pattern': hyphenated,
                        'attr': term['attr'],
                        'replace': replace if replace else term['pattern'],
                        'category': term['category'],
                        'pos': 'PROPN',
                    })

    def itis_common_names(
            self,
            taxon: str,
            kingdom_id: int = 5,
            rank_id: int = 220,
            replace: bool = False
    ) -> None:
        """Guides often use common names instead of scientific name.

        kingdom_id =   5 == Animalia
        rank_id    = 220 == Species
        """
        if not ITIS_DB.exists():
            print('Could not find ITIS database.')
            self.mock_itis_traits(taxon)
            return

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
            self.terms.append(term)

    def drop(self, excludes: Union[str, List[str]], field: str = 'label') -> None:
        """Drop terms from the traits.

        If we include terms that interfere with patterns we can drop them.
        """
        excludes = excludes.split() if isinstance(excludes, str) else excludes
        self.terms = [t for t in self.terms if t[field] not in excludes]

    def mock_itis_traits(
            self, name: str, mock_terms_csv: Optional[Union[str, Path]] = None
    ) -> None:
        """Set up mock traits for testing with Travis.

        The ITIS database is too big to put into GitHub so we use a mock database
        for testing.
        """
        if not mock_terms_csv:
            mock_terms_csv = VOCAB_DIR / 'mock_itis_terms.csv'

        name = name.lower()

        with open(mock_terms_csv) as term_file:
            reader = csv.DictReader(term_file)
            terms = list(reader)

        for term in terms:
            label = term['label']
            term['label'] = label if label else name

        self.terms += terms
