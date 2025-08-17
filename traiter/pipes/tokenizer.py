"""
Update the tokenizer.

The default Spacy tokenizer works great for model-based parsing but sometimes causes
complications for rule-based parsers.
"""

import csv
import re
import string
from pathlib import Path

from spacy.lang.char_classes import ALPHA, LIST_HYPHENS, LIST_PUNCT, LIST_QUOTES
from spacy.language import Language
from spacy.util import compile_infix_regex, compile_prefix_regex, compile_suffix_regex

from traiter.rules import terms

BREAKING = LIST_QUOTES + LIST_PUNCT + [r"[:\\/˂˃×.+’()\[\]±_]"]

DASHES = "|".join(re.escape(h) for h in LIST_HYPHENS if len(h) == 1)
DASHES = f"(?:{DASHES})+"

PREFIX: list[str] = [*BREAKING, DASHES + "(?=[0-9])", "x(?=[0-9])"]
SUFFIX: list[str] = [*BREAKING, DASHES]

INFIX: list[str] = [
    rf"(?<=[{ALPHA}0-9])[,.:<>=/+](?=[{ALPHA}])",  # word=word
    rf"(?<=[{ALPHA}])[,.:<>=/+](?=[{ALPHA}0-9])",  # word=word
    rf"(?<=[{ALPHA}])[,.:<>=/+]",  # word,
    r"""[\\\[\]()/:;’'"“”'+±_]""",  # Break on these characters
    DASHES,
    rf"(?<=\d)[{ALPHA}]+",  # Digit to letters like: 8m
]

ABBREVS: list[str] = """
    Var. Sect. Subsect. Ser. Subser. Subsp. Spec. Sp. Spp.
    var. sect. subsect. ser. subser. subsp. spec. sp. spp. nov.
    """.split()
ABBREVS += [f"{c}." for c in string.ascii_uppercase]


def append_prefix_regex(nlp: Language, prefixes: list[str] | None = None) -> None:
    prefixes = prefixes if prefixes else []
    prefixes += nlp.Defaults.prefixes
    prefix_re = compile_prefix_regex(prefixes)
    nlp.tokenizer.prefix_search = prefix_re.search


def append_suffix_regex(nlp: Language, suffixes: list[str] | None = None) -> None:
    suffixes = suffixes if suffixes else []
    suffixes += nlp.Defaults.suffixes
    suffix_re = compile_suffix_regex(suffixes)
    nlp.tokenizer.suffix_search = suffix_re.search


def append_infix_regex(nlp: Language, infixes: list[str] | None = None) -> None:
    infixes = infixes if infixes else []
    infixes += nlp.Defaults.infixes
    infix_re = compile_infix_regex(infixes)
    nlp.tokenizer.infix_finditer = infix_re.finditer


def append_abbrevs(nlp: Language, abbrevs: list[str]) -> None:
    for abbrev in abbrevs:
        nlp.tokenizer.add_special_case(abbrev, [{"ORTH": abbrev}])


def remove_special_case(nlp: Language, remove: list[str]):
    """
    Remove special rules from the tokenizer.

    This is a workaround for when these special cases interfere with matcher rules.
    """
    specials = (r for r in nlp.tokenizer.rules if r not in remove)
    nlp.tokenizer.rules = None
    for text in specials:
        nlp.tokenizer.add_special_case(text, [{"ORTH": text}])


def get_states():
    path = Path(terms.__file__).parent / "us_location_terms.csv"
    with path.open(encoding="utf8") as in_file:
        reader = csv.DictReader(in_file)
        return {t["pattern"] for t in reader if t["label"] == "us_state"}


def setup_tokenizer(nlp):
    append_prefix_regex(nlp, PREFIX)
    append_infix_regex(nlp, INFIX)
    append_suffix_regex(nlp, SUFFIX)
    append_abbrevs(nlp, ABBREVS)
    # Remove patterns that interfere with parses
    states = get_states()
    removes = []
    for rule in nlp.tokenizer.rules:
        if re.search(r"\d", rule):
            removes.append(rule)
        if rule.lower() in states:
            removes.append(rule)
        if rule in ("'s", "'S"):
            removes.append(rule)
    remove_special_case(nlp, removes)
