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
import copy
import csv
from io import TextIOWrapper
from pathlib import Path
from typing import Any
from zipfile import ZipFile

from . import const


class TermList:  # (UserList):
    def __init__(self, terms: list[dict] = None):
        self._terms = terms if terms else []
        self.replace = {}

    def __add__(self, other):
        if not isinstance(other, TermList):
            raise ValueError("Can only add another TermList")
        new = TermList(self.terms)
        new.terms += other.terms
        return new

    def __iadd__(self, other):
        if not isinstance(other, TermList):
            raise ValueError("Can only add another TermList")
        self.terms += other.terms
        return self

    @property
    def terms(self):
        return self._terms

    @terms.setter
    def terms(self, values):
        self.set_replace()
        self.validate_terms(values)
        self._terms = self.filter_duplicates(values)

    def set_replace(self):
        self.replace = {t["pattern"]: r for t in self.terms if (r := t.get("replace"))}

    @staticmethod
    def validate_terms(values):
        for term in values:
            if not term.get("label") or not term.get("pattern"):
                raise ValueError("Both: 'label' and 'pattern' are required fields")
            term["attr"] = term.get("attr", "lower")

    @staticmethod
    def filter_duplicates(values):
        """Filter out duplicate terms.

        If we try to add the same term list more than once or have overlapping term
        lists remove the duplicates. Only an error if we are using the same pattern
        with a different label.
        """
        used = {}
        unique = []
        for term in values:
            key = term["pattern"]
            if key in used:
                new = term["label"]
                old = used["label"]
                if old != new:
                    raise ValueError(f"Pattern {key} is used for both {old} and {new}")
                continue
            unique.append(term)
        return unique

    def read(self, path: Path, member=""):
        """Read terms from a possibly zipped CSV file."""
        if path.suffix == ".zip":
            member = member if member else f"{path.stem}.csv"
            with ZipFile(path) as zippy:
                with zippy.open(member) as in_csv:
                    reader = csv.DictReader(TextIOWrapper(in_csv, "utf-8"))
                    terms = list(reader)
        else:
            with open(path) as term_file:
                reader = csv.DictReader(term_file)
                terms = list(reader)

        self.terms += terms
        return self

    def shared(self, file_stems: str):
        """Read a CSV from the traiter vocabulary."""
        file_stems = file_stems.split() if isinstance(file_stems, str) else file_stems
        for stem in file_stems:
            path = const.VOCAB_DIR / f"{stem}.csv"
            self.read(path)
        return self

    def add_trailing_dash(self):
        new = []
        for term in self.terms:
            if term["pattern"][-1] != "-":
                new_term = copy.deepcopy(term)
                new_term["pattern"] += "-"
                new.append(new_term)
        self.terms += new
        return self

    def drop(self, drops: str | list[str], field: str = "label"):
        """Drop term from the traits.

        If we include terms that interfere with patterns we can drop them. For instance,
        'in' may be an inch abbreviation or a preposition, so we could:
        term.drop('in', field='pattern') or we can drop imperial_units altogether with
        term.drop('imperial_length').
        """
        drops = drops.split() if isinstance(drops, str) else drops
        self.terms = [t for t in self.terms if t[field] not in drops]
        # self.set_replace()
        return self

    def pick(self, takes: str | list[str]):
        """Only select terms with the given labels from the CSV file."""
        takes = takes.split() if isinstance(takes, str) else takes
        terms = [t for t in self.terms if t["label"] in takes]
        return TermList(terms)

    def split(self, takes: str | list[str], field: str = "label"):
        """Take selected terms from one trait list and return and return a new list."""
        takes = takes.split() if isinstance(takes, str) else takes
        terms = [t for t in self.terms if t[field] in takes]
        return TermList(terms)

    def pattern_dict(self, column: str, type_=None) -> dict[str, Any]:
        """Create a dict key = pattern,  value = another column value."""
        return self.column_dict("pattern", column, type_)

    def column_dict(self, key: str, value: str, type_=None) -> dict[str, Any]:
        """Create a dictionary between any 2 columns of terms."""
        type_ = type_ if type_ else str
        dict_ = {
            t[key]: type_(t[value]) for t in self.terms if t.get(key) and t.get(value)
        }
        return dict_

    def labels(self):
        """Get all labels for the terms."""
        lbs = {t["label"] for t in self.terms}
        return sorted(lbs)
