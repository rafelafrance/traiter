"""Update the tokenizer.

The default Spacy tokenizer works great for model-based parsing but sometimes causes
complications for rule-based parsers.
"""

from typing import Optional

from spacy.lang.char_classes import (
    ALPHA, HYPHENS, LIST_HYPHENS, LIST_PUNCT, LIST_QUOTES)
from spacy.language import Language
from spacy.util import compile_infix_regex, compile_prefix_regex, compile_suffix_regex

# These rules were useful in the past
DASHES = [h for h in LIST_HYPHENS if len(h) == 1]
BREAKING = LIST_QUOTES + LIST_PUNCT + DASHES
BREAKING += r""" \\ / ˂ ˃ × [.] [\+] """.split()
PREFIX = SUFFIX = BREAKING

# These rules were useful in the past
INFIX = [
    fr'(?<=[{ALPHA}0-9])[:<>=/+](?=[{ALPHA}])',
    fr"""(?:{HYPHENS})""",              # Break on any hyphen
    r"""[\\\[\]\(\)/:;’'“”'+]""",       # Break on these characters
    fr'(?<=[0-9])\.?(?=[{ALPHA}])',     # 1.word or 1N
    fr'(?<=[{ALPHA}]),(?=[0-9])',       # word,digits
]


def append_prefix_regex(nlp: Language, prefixes: Optional[list[str]] = None):
    """Append to the breaking prefix rules."""
    prefixes = prefixes if prefixes else PREFIX
    prefixes += nlp.Defaults.prefixes
    prefixes = set(prefixes)
    prefix_re = compile_prefix_regex(prefixes)
    nlp.tokenizer.suffix_search = prefix_re.search


def append_suffix_regex(nlp: Language, suffixes: Optional[list[str]] = None):
    """Append to the breaking prefix rules."""
    suffixes = suffixes if suffixes else SUFFIX
    suffixes += nlp.Defaults.suffixes
    suffixes = set(suffixes)
    suffix_re = compile_suffix_regex(suffixes)
    nlp.tokenizer.suffix_search = suffix_re.search


def append_infix_regex(nlp: Language, infixes: Optional[list[str]] = None):
    """Append to the breaking prefix rules."""
    infixes = infixes if infixes else INFIX
    infixes += nlp.Defaults.infixes
    infixes = set(infixes)
    infix_re = compile_infix_regex(infixes)
    nlp.tokenizer.infix_finditer = infix_re.finditer


def append_tokenizer_regexes(
        nlp: Language,
        prefixes: Optional[list[str]] = None,
        infixes: Optional[list[str]] = None,
        suffixes: Optional[list[str]] = None
):
    """Append all three prefix, infix, suffix."""
    append_prefix_regex(nlp, prefixes)
    append_infix_regex(nlp, infixes)
    append_suffix_regex(nlp, suffixes)


def append_abbrevs(nlp: Language, special_cases: list[str], attr: str = 'ORTH'):
    """Add special case tokens to the tokenizer."""
    for case in special_cases:
        nlp.tokenizer.add_special_case(case, [{attr: case}])
