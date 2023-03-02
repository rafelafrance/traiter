"""A term base class.

Columns for a vocabulary CSV file:
    Required columns:
        label   = the term's hypernym, 'color' is a hypernym of 'blue'
        pattern = the term itself
        attr    = the spaCy attribute being matched upon, this is typically
            'lower' but sometimes 'regex' or 'text' is used. The default is 'lower'.
    Optional columns:
        replace   = Replace the match with this
        hyphenate = A custom hyphenation scheme for the pattern
        and more...
"""
import csv
from pathlib import Path
from typing import Any

from hyphenate import hyphenate_word

from . import const


HYPHENS = ("-", "\xad")

StrList = str | list[str]


def shared(file_stem: str, dir_: Path = None) -> list[dict]:
    dir_ = dir_ if dir_ else const.VOCAB_DIR
    path = dir_ / f"{file_stem}.csv"
    return read(path)


def read(path: Path) -> list[dict]:
    with open(path) as term_file:
        reader = csv.DictReader(term_file)
        terms = list(reader)

    for term in terms:
        term["attr"] = term.get("attr", "lower")

    return terms


def pattern_dict(terms: list[dict], column: str, type_=None) -> dict[str, Any]:
    """Create a dict key = pattern,  value = another column value."""
    type_ = type_ if type_ else str
    return {t["pattern"]: type_(t[column]) for t in terms if t.get(column)}


def drop(terms: list[dict], drops: StrList, field: str = "label") -> list[dict]:
    """Drop term from the traits.

    If we include terms that interfere with patterns we can drop them. For instance,
    'in' may be an inch abbreviation or a preposition, so we could:
    term.drop('in', field='pattern').
    """
    drops = drops.split() if isinstance(drops, str) else drops
    return [t for t in terms if t[field] not in drops]


def hyphenate(terms: list[dict]) -> list[dict]:
    """Systematically handle hyphenated terms.

    We cannot depend on terms being present in a contiguous form (e.g. web pages).
    We need a systematic method for handling hyphenated terms. The Hyphenate
    library is great for this, but sometimes we need to handle non-standard
    hyphenations manually. Non-standard hyphenations are stored with the terms.
    """
    new = []
    for term in terms:

        if term.get("hyphenate"):
            # Handle a non-standard hyphenation
            parts = term["hyphenate"].split("-")
        else:
            # A standard hyphenation
            parts = hyphenate_word(term["pattern"])

        for i in range(1, len(parts)):
            replace = term.get("replace")
            for hyphen in HYPHENS:
                hyphenated = "".join(parts[:i]) + hyphen + "".join(parts[i:])
                new.append(
                    {
                        **term,
                        **{
                            "label": term["label"],
                            "pattern": hyphenated,
                            "attr": term["attr"],
                            "replace": replace if replace else term["pattern"],
                        },
                    }
                )
    return new
