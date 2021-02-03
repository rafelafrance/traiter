"""Get terms from various sources like CSV files or an SQLite database.

Columns for a vocabulary CSV file:
    Required columns:
        label   = the term's hypernym, 'color' is a hypernym of 'blue'
        pattern = the term itself
        attr    = the spaCy attribute being matched upon, this is typically
            'lower' but sometimes 'regex' or 'text' is used. The default is 'lower'.
    Optional columns:
        replace   = Replace the match with this
        hyphenate = A custom hyphenation scheme for the pattern
"""

import csv
from pathlib import Path
from typing import Optional, Union

from hyphenate import hyphenate_word

from ..const import DASH_CHAR
import traiter.vocabulary as vocab

# This points to the traiter vocabulary files
SHARED_CSV = list(Path(vocab.__file__).parent.glob('*.csv'))

HYPHENS = ('-', '\xad')

StrList = Union[str, list[str]]
PathList = Union[str, list[str], Path, list[Path]]
OptStrList = Optional[StrList]


class Csv:
    """A dictionary of terms."""

    def __init__(self, terms: Optional[list[dict]] = None) -> None:
        self.terms = terms if terms else []

    def __iter__(self):
        yield from self.terms

    def __add__(self, other: 'Csv') -> 'Csv':
        self.terms += other.terms
        return self

    def with_pattern(self, pattern: str = ''):
        """Given a pattern get the term."""
        terms = [t for t in self.terms if t['pattern'] == pattern]
        return terms

    def with_label(self, label: str = ''):
        """Given a pattern get the term."""
        terms = [t for t in self.terms if t['label'] == label]
        return terms

    def drop(self, drops: StrList, field: str = 'label') -> None:
        """Drop term from the traits.

        If we include terms that interfere with patterns we can drop them.
        For instance, 'in' can be either an inch abbreviation term which may interfere
        with a preposition so we could: term.drop('in', field='pattern').
        """
        drops = drops.split() if isinstance(drops, str) else drops
        self.terms = [t for t in self.terms if t[field] not in drops]

    def for_entity_ruler(self, attr: str = 'LOWER'):
        """Return ruler pattens from the terms."""
        attr = attr.upper()
        rules = [{'label': t['label'], 'pattern': t['pattern']}
                 for t in self.terms if t['attr'].upper() == attr]
        return rules

    def pattern_dict(self, column: str) -> dict[str, dict]:
        """Create a dict from a column in the terms."""
        return {t['pattern']: v for t in self.terms
                if (v := t.get(column)) not in (None, '')}

    ###########################################################################
    # Other constructors

    @classmethod
    def read_csv(cls, paths: PathList, labels: OptStrList = None) -> 'Csv':
        """Read a CSV file."""
        terms = cls()

        if isinstance(paths, str):
            paths = paths.split()
        elif isinstance(paths, Path):
            paths = [paths]

        for path in paths:
            with open(path) as term_file:
                reader = csv.DictReader(term_file)
                new_terms = list(reader)

            if labels:
                labels = labels if isinstance(labels, list) else labels.split()
                new_terms = [t for t in new_terms if t['label'] in labels]

            for term in new_terms:
                if not term.get('attr'):
                    term['attr'] = 'lower'

            terms += cls(terms=new_terms)

        return terms

    @classmethod
    def shared(cls, names: StrList, labels: OptStrList = None) -> 'Csv':
        """Get the path to a shared vocabulary file.
            shared: Names (possibly abbreviated) of the the shared files to include.
            label:  A list of labels to include from the files. None = all
        """
        names = names.split() if isinstance(names, str) else names
        labels = labels.split() if isinstance(labels, str) else labels

        terms = cls()

        for name in names:

            path_set = {s for s in SHARED_CSV if s.name.lower().startswith(name)}

            if not path_set:
                err = f'\nShared terms "{name}" not found in: '
                err += ' '.join(f'"{s.stem}"' for s in SHARED_CSV)
                raise Exception(err)

            path = path_set.pop()

            terms += cls.read_csv(path, labels)

        return terms

    @classmethod
    def hyphenate_terms(cls, other: 'Csv') -> 'Csv':
        """Systematically handle hyphenated terms.

        We cannot depend on terms being present in a contiguous form. We need a
        systematic method for handling hyphenated terms. The hyphenate library is
        great for this but sometimes we need to handle non-standard hyphenations
        manually. Non-standard hyphenations are stored in the terms CSV file.
        """
        terms = []
        for term in other.terms:

            if term.get('hyphenate'):
                # Handle a non-standard hyphenation
                parts = term['hyphenate'].split('-')
            else:
                # A standard hyphenation
                parts = hyphenate_word(term['pattern'])

            for i in range(1, len(parts)):
                replace = term.get('replace')
                for hyphen in HYPHENS:
                    hyphenated = ''.join(parts[:i]) + hyphen + ''.join(parts[i:])
                    terms.append({**term, **{
                        'label': term['label'],
                        'pattern': hyphenated,
                        'attr': term['attr'],
                        'replace': replace if replace else term['pattern'],
                    }})
        return cls(terms=terms)

    @classmethod
    def trailing_dash(cls, other: 'Csv', label: str) -> 'Csv':
        """Systematically handle hyphenated terms.

        We cannot depend on terms being present in a contiguous form. We need a
        systematic method for handling hyphenated terms. The hyphenate library is
        great for this but sometimes we need to handle non-standard hyphenations
        manually. Non-standard hyphenations are stored in the terms CSV file.
        """
        terms = []
        for term in other.terms:
            pattern = term['pattern']
            if term.get('label') == label and pattern[-1] not in DASH_CHAR:
                replace = term.get('replace')
                for dash in DASH_CHAR:
                    terms.append({**term, **{
                        'pattern': pattern + dash,
                        'replace': replace if replace else pattern,
                    }})
        return cls(terms=terms)

    @classmethod
    def pick_words(
            cls,
            other: 'Csv',
            old_label: str,
            idx: Union[int, list[int], tuple[int]],
            new_label: str = None,
            attr: str = 'lower'
    ) -> 'Csv':
        """Create a new term by picking a words from an old term.

        Used to get species or genus names like: 'Canis lupus' -> 'lupus'.
        """
        terms = []
        idx = (idx, idx + 1) if isinstance(idx, int) else idx
        new_label = new_label if new_label else old_label

        used_patterns = set()

        for term in [t for t in other.terms if t['label'] == old_label]:
            words = term['pattern'].split()

            if len(words) >= idx[1]:
                pattern = ' '.join(words[idx[0]:idx[1]])

                if pattern not in used_patterns:
                    terms.append({**term, **{
                        'label': new_label,
                        'pattern': pattern,
                        'attr': attr,
                    }})
                    used_patterns.add(pattern)
        return cls(terms=terms)

    @classmethod
    def abbrev_terms(
            cls, other: 'Csv', label: str, idx: int = 0, attr='lower', suffix='.'
    ) -> 'Csv':
        """Create an abbreviated term from another term.

        For example an abbreviated species: 'Canis lupus' -> 'C. lupus'.
        """
        terms = []
        used_patterns = set()

        for term in other.terms:
            if term['label'] == label:
                old_pattern = term['pattern']
                words = old_pattern.split()
                if len(words) > idx and words[idx][-1] != suffix:
                    words[idx] = words[idx][0] + suffix
                    new_pattern = ' '.join(words)
                    if new_pattern not in used_patterns:
                        terms.append({**term, **{
                            'label': label,
                            'pattern': new_pattern,
                            'attr': attr,
                            'replace': old_pattern,
                        }})
                        used_patterns.add(new_pattern)
        return cls(terms=terms)
