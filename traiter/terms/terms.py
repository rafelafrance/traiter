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
import logging
from typing import Any
from typing import Optional
from typing import Union

from hyphenate import hyphenate_word

from .. import const

HYPHENS = ("-", "\xad")

StrList = Union[str, list[str]]


class Terms:
    """A dictionary of terms."""

    def __init__(self, terms: Optional[list[dict]] = None) -> None:
        terms = terms if terms else []
        self.terms = []
        self.patterns = {}
        self.no_clobber = True
        self.silent = True
        self.add_terms(terms)

    def add_terms(self, terms):
        """Add terms while respecting the no clobber flag."""
        if self.no_clobber:
            for term in terms:
                lower = term["pattern"].lower()
                if lower not in self.patterns:
                    self.terms.append(term)
                    self.patterns[lower] = term["label"]
                elif not self.silent:
                    msg = "%s in %s already exists in %s."
                    logging.warning(
                        msg, term["pattern"], term["label"], self.patterns[lower]
                    )
        else:
            self.terms += terms

    def __iter__(self):
        yield from self.terms

    def __add__(self, other: "Terms") -> "Terms":
        self.add_terms(other.terms)
        return self

    def with_label(self, label: str = "") -> list[dict]:
        """Given a label get the terms."""
        terms = [t for t in self.terms if t["label"] == label]
        return terms

    def patterns_with_label(self, label: str = "") -> list[str]:
        """Get all patterns with the given label."""
        return [t["pattern"] for t in self.with_label(label)]

    def drop(self, drops: StrList, field: str = "label") -> None:
        """Drop term from the traits.

        If we include terms that interfere with patterns we can drop them.
        For instance, 'in' can be either an inch abbreviation term which may interfere
        with a preposition so we could: term.drop('in', field='pattern').
        """
        drops = drops.split() if isinstance(drops, str) else drops
        self.terms = [t for t in self.terms if t[field] not in drops]
        self.patterns = {t["pattern"]: t["label"] for t in self.terms}

    def for_entity_ruler(self, attr: str = "LOWER"):
        """Return ruler pattens from the terms."""
        attr = attr.upper()
        rules = [
            {"label": t["label"], "pattern": t["pattern"]}
            for t in self.terms
            if t["attr"].upper() == attr
        ]
        return rules

    def pattern_dict(self, column: str) -> dict[str, Any]:
        """Create a dict from a column in the terms."""
        return {
            t["pattern"]: val
            for t in self.terms
            if (val := t.get(column)) not in (None, "")
        }

    ###########################################################################
    # Other constructors

    @classmethod
    def hyphenate_terms(cls, other: "Terms") -> "Terms":
        """Systematically handle hyphenated terms.

        We cannot depend on terms being present in a contiguous form. We need a
        systematic method for handling hyphenated terms. The hyphenate library is
        great for this but sometimes we need to handle non-standard hyphenations
        manually. Non-standard hyphenations are stored in the terms CSV file.
        """
        terms = []
        for term in other.terms:

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
                    terms.append(
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
        return cls(terms=terms)

    @classmethod
    def trailing_dash(cls, other: "Terms", label: str) -> "Terms":
        """Systematically handle hyphenated terms.

        We cannot depend on terms being present in a contiguous form. We need a
        systematic method for handling hyphenated terms. The hyphenate library is
        great for this but sometimes we need to handle non-standard hyphenations
        manually. Non-standard hyphenations are stored in the terms CSV file.
        """
        terms = []
        for term in other.terms:
            pattern = term["pattern"]
            if term.get("label") == label and pattern[-1] not in const.DASH_CHAR:
                replace = term.get("replace")
                for dash in const.DASH_CHAR:
                    terms.append(
                        {
                            **term,
                            **{
                                "pattern": pattern + dash,
                                "replace": replace if replace else pattern,
                            },
                        }
                    )
        return cls(terms=terms)

    @classmethod
    def abbrev_terms(
        cls, other: "Terms", label: str, idx: int = 0, attr="lower", suffix="."
    ) -> "Terms":
        """Create an abbreviated term from another term.
        For example an abbreviated species: 'Canis lupus' -> 'C. lupus'.
        """
        terms = []
        used_patterns = set()

        for term in other.terms:
            if term["label"] == label:
                old_pattern = term["pattern"]
                words = old_pattern.split()
                if len(words) > idx and words[idx][-1] != suffix:
                    words[idx] = words[idx][0] + suffix
                    new_pattern = " ".join(words)
                    if new_pattern not in used_patterns:
                        terms.append(
                            {
                                **term,
                                **{
                                    "label": label,
                                    "pattern": new_pattern,
                                    "attr": attr,
                                    "replace": old_pattern,
                                },
                            }
                        )
                        used_patterns.add(new_pattern)
        return cls(terms=terms)

    @classmethod
    def pick_words(
        cls,
        other: "Terms",
        old_label: str,
        idx: Union[int, list[int], tuple],
        new_label: str = None,
        attr: str = "lower",
    ) -> "Terms":
        """Create a new term by picking a words from an old term.
        Used to get species or genus names like: 'Canis lupus' -> 'lupus'.
        """
        terms = []
        idx = (idx, idx + 1) if isinstance(idx, int) else idx
        new_label = new_label if new_label else old_label

        used_patterns = set()

        for term in [t for t in other.terms if t["label"] == old_label]:
            words = term["pattern"].split()

            if len(words) >= idx[1]:
                pattern = " ".join(words[idx[0] : idx[1]])

                if pattern not in used_patterns:
                    terms.append(
                        {
                            **term,
                            **{
                                "label": new_label,
                                "pattern": pattern,
                                "attr": attr,
                            },
                        }
                    )
                    used_patterns.add(pattern)
        return cls(terms=terms)
