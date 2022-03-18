"""Update the tokenizer.

The default Spacy tokenizer works great for model-based parsing but sometimes causes
complications for rule-based parsers.
"""

from typing import Optional

from spacy.lang.char_classes import ALPHA, LIST_HYPHENS, LIST_PUNCT, LIST_QUOTES
from spacy.language import Language
from spacy.util import compile_infix_regex, compile_prefix_regex, compile_suffix_regex

from traiter.util import list_to_char_class

# These rules were useful in the past
DASHES = [h for h in LIST_HYPHENS if len(h) == 1]
DASH_CLASS = list_to_char_class(DASHES)
BREAKING = LIST_QUOTES + LIST_PUNCT + DASHES
BREAKING += r""" [\\/˂˃×.+] """.split()
PREFIX = SUFFIX = BREAKING

# These rules were useful in the past
INFIX = [
    fr'(?<=[{ALPHA}0-9])[:<>=/+](?=[{ALPHA}])',
    fr"""{DASH_CLASS}""",  # Break on any hyphen
    r"""[\\\[\]\(\)/:;’'“”'+]""",  # Break on these characters
    fr'(?<=[0-9])\.?(?=[{ALPHA}])',  # 1.word or 1N
    fr'(?<=[{ALPHA}]),(?=[0-9])',  # word,digits
]


def append_prefix_regex(nlp: Language, prefixes: Optional[list[str]] = None):
    """Append to the breaking prefix rules."""
    prefixes2 = prefixes if prefixes else PREFIX
    prefixes2 += nlp.Defaults.prefixes
    prefixes3 = set(prefixes2)
    prefix_re = compile_prefix_regex(prefixes3)
    nlp.tokenizer.suffix_search = prefix_re.search


def append_suffix_regex(nlp: Language, suffixes: Optional[list[str]] = None):
    """Append to the breaking prefix rules."""
    suffixes2 = suffixes if suffixes else SUFFIX
    suffixes2 += nlp.Defaults.suffixes
    suffixes3 = set(suffixes2)
    suffix_re = compile_suffix_regex(suffixes3)
    nlp.tokenizer.suffix_search = suffix_re.search


def append_infix_regex(nlp: Language, infixes: Optional[list[str]] = None):
    """Append to the breaking prefix rules."""
    infixes2 = infixes if infixes else INFIX
    infixes2 += nlp.Defaults.infixes
    infixes3 = set(infixes2)
    infix_re = compile_infix_regex(infixes3)
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
