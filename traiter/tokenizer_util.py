"""Update the tokenizer.

The default Spacy tokenizer works great for model-based parsing but sometimes causes
complications for rule-based parsers.
"""
from typing import Iterable
from typing import Optional

import regex as re
from spacy.lang.char_classes import ALPHA
from spacy.lang.char_classes import LIST_HYPHENS
from spacy.lang.char_classes import LIST_PUNCT
from spacy.lang.char_classes import LIST_QUOTES
from spacy.language import Language
from spacy.symbols import ORTH
from spacy.util import compile_infix_regex
from spacy.util import compile_prefix_regex
from spacy.util import compile_suffix_regex

# These rules were useful in the past
DASHES = "|".join(re.escape(h) for h in LIST_HYPHENS)
DASHES = f"(?:{DASHES})+"

BREAKING = LIST_QUOTES + LIST_PUNCT + r""" [:\\/˂˃×.+’] """.split()

PREFIXES = BREAKING + [DASHES + "(?=[0-9])"]
SUFFIXES = BREAKING + [DASHES]

# These rules were useful in the past
INFIXES = [
    fr"(?<=[{ALPHA}0-9])[:<>=/+](?=[{ALPHA}])",
    fr"""{DASHES}""",  # Break on any hyphen
    r"""[\\\[\]\(\)/:;’'“”'+]""",  # Break on these characters
    fr"(?<=[0-9])\.?(?=[{ALPHA}])",  # 1.word or 1N
    fr"(?<=[{ALPHA}]),(?=[0-9])",  # word,digits
]


def append_prefix_regex(
    nlp: Language, prefixes: Optional[list[str]] = None, replace: bool = False
):
    """Append to the breaking prefix rules."""
    prefixes = prefixes if prefixes else []
    if not replace:
        prefixes += PREFIXES
    prefixes += nlp.Defaults.prefixes
    prefix_re = compile_prefix_regex(prefixes)
    nlp.tokenizer.prefix_search = prefix_re.search


def append_suffix_regex(
    nlp: Language, suffixes: Optional[list[str]] = None, replace: bool = False
):
    """Append to the breaking prefix rules."""
    suffixes = suffixes if suffixes else []
    if not replace:
        suffixes += SUFFIXES
    suffixes += nlp.Defaults.suffixes
    suffix_re = compile_suffix_regex(suffixes)
    nlp.tokenizer.suffix_search = suffix_re.search


def append_infix_regex(
    nlp: Language, infixes: Optional[list[str]] = None, replace: bool = False
):
    """Append to the breaking prefix rules."""
    infixes = infixes if infixes else []
    if not replace:
        infixes += INFIXES
    infixes += nlp.Defaults.infixes
    infix_re = compile_infix_regex(infixes)
    nlp.tokenizer.infix_finditer = infix_re.finditer


def append_tokenizer_regexes(
    nlp: Language,
    prefixes: Optional[list[str]] = None,
    infixes: Optional[list[str]] = None,
    suffixes: Optional[list[str]] = None,
):
    """Append all three prefix, infix, suffix."""
    append_prefix_regex(nlp, prefixes)
    append_infix_regex(nlp, infixes)
    append_suffix_regex(nlp, suffixes)


def append_abbrevs(nlp: Language, special_cases: list[str]):
    """Add special case tokens to the tokenizer."""
    for case in special_cases:
        nlp.tokenizer.add_special_case(case, [{ORTH: case}])


def add_special_case(nlp: Language, special_cases: list[Iterable]):
    """Add special case tokens to the tokenizer."""
    for case in special_cases:
        text, *parts = case
        rule = [{ORTH: p} for p in parts]
        nlp.tokenizer.add_special_case(text, rule)


def remove_special_case(nlp: Language, remove: list[dict]):
    """Remove special rules from the tokenizer.

    This is a workaround for when these special cases interfere with matcher rules.
    """
    remove = {r["pattern"].lower() for r in remove}
    specials = [(r, r) for r in nlp.tokenizer.rules if r.lower() not in remove]
    nlp.tokenizer.rules = None
    add_special_case(nlp, specials)
