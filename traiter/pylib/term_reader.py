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
from pathlib import Path
from typing import Any

from . import const


def read(path: Path) -> list[dict]:
    with open(path) as term_file:
        reader = csv.DictReader(term_file)
        terms = list(reader)

    for term in terms:
        term["attr"] = term.get("attr", "lower")

    return terms


def shared(file_stem: str, dir_: Path = None) -> list[dict]:
    dir_ = dir_ if dir_ else const.VOCAB_DIR
    path = dir_ / f"{file_stem}.csv"
    return read(path)


def pattern_dict(terms: list[dict], column: str, type_=None) -> dict[str, Any]:
    """Create a dict key = pattern,  value = another column value."""
    type_ = type_ if type_ else str
    return {t["pattern"]: type_(t[column]) for t in terms if t.get(column)}


def drop(terms: list[dict], drops: str | list[str], field: str = "label") -> list[dict]:
    """Drop term from the traits.

    If we include terms that interfere with patterns we can drop them. For instance,
    'in' may be an inch abbreviation or a preposition, so we could:
    term.drop('in', field='pattern').
    """
    drops = drops.split() if isinstance(drops, str) else drops
    return [t for t in terms if t[field] not in drops]
