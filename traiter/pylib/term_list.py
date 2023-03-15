"""A term base class.

Columns for a vocabulary CSV file:
    Required columns:
        label   = the term's hypernym, 'color' is a hypernym of 'blue'
        pattern = the term itself
        attr    = the spaCy attribute being matched upon, this is typically 'lower' but
            sometimes 'regex' or 'text' is used. The default is 'lower'.
    Optional columns:
        replace   = Replace the match with this
        and more...
"""
import csv
from collections import UserList
from pathlib import Path
from typing import Any

from . import const


class TermList(UserList):
    def __init__(self, lst):
        super().__init__(lst)
        self.replace = {t["pattern"]: r for t in self if (r := t.get("replace"))}

    @staticmethod
    def _read(path: Path):
        with open(path) as term_file:
            reader = csv.DictReader(term_file)
            terms = list(reader)

        for term in terms:
            term["attr"] = term.get("attr", "lower")

        return terms

    @classmethod
    def read(cls, path: Path):
        """Read terms from a CSV file."""
        terms = cls.read(path)
        return cls(terms)

    @classmethod
    def pick(cls, path: Path, takes: str | list[str]):
        """Only select terms with the given labels from the CSV file."""
        terms = cls._read(path)
        takes = takes.split() if isinstance(takes, str) else takes
        terms = [t for t in terms if t["label"] in takes]
        return cls(terms)

    @classmethod
    def pick_shared(cls, file_stem: str, takes: str | list[str]):
        path = const.VOCAB_DIR / f"{file_stem}.csv"
        return cls.pick(path, takes)

    @classmethod
    def shared(cls, file_stem: str):
        """Read a CSV from the traiter vocabulary."""
        path = const.VOCAB_DIR / f"{file_stem}.csv"
        terms = cls._read(path)
        return cls(terms)

    @classmethod
    def split(cls, terms, takes: str | list[str], field: str = "label"):
        """Take terms from another trait list."""
        takes = takes.split() if isinstance(takes, str) else takes
        terms = [t for t in terms if t[field] in takes]
        return cls(terms)

    def pattern_dict(self, column: str, type_=None) -> dict[str, Any]:
        """Create a dict key = pattern,  value = another column value."""
        type_ = type_ if type_ else str
        patterns = {t["pattern"]: type_(t[column]) for t in self if t.get(column)}
        return patterns

    def drop(self, drops: str | list[str], field: str = "label"):
        """Drop term from the traits.

        If we include terms that interfere with patterns we can drop them. For instance,
        'in' may be an inch abbreviation or a preposition, so we could:
        term.drop('in', field='pattern').
        """
        drops = drops.split() if isinstance(drops, str) else drops
        self.data = [t for t in self if t[field] not in drops]
