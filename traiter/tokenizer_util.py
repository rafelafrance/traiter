"""Update the tokenizer.

The default Spacy tokenizer works great for model-based parsing but sometimes causes
complications for rule-based parsers.
"""

from typing import List, Optional

from spacy.lang.char_classes import (
    ALPHA, HYPHENS, LIST_HYPHENS, LIST_PUNCT, LIST_QUOTES)
from spacy.language import Language
from spacy.util import compile_infix_regex, compile_prefix_regex, compile_suffix_regex

# These rules were useful in the past
BREAKING = LIST_QUOTES + LIST_HYPHENS + LIST_PUNCT
BREAKING += """ \\ / ˂ ˃ × """.split()

# These rules were useful in the past
INFIX = [
    r'(?<=[{a}0-9])[:<>=/+](?=[{a}])'.format(a=ALPHA),
    r"""(?:{h})+""".format(h=HYPHENS),  # Break on any hyphen
    r"""[\\\[\]\(\)/:;’'“”'+]""",  # Break on these characters
    r'(?<=[0-9])\.?(?=[{a}])'.format(a=ALPHA),  # 1.word or 1N
    r'(?<=[{a}]),(?=[0-9])'.format(a=ALPHA),  # word,digits
]


def append_prefix_regex(nlp: Language, prefixes: Optional[List[str]] = None):
    """Append to the breaking prefix rules."""
    prefixes = prefixes if prefixes else BREAKING
    prefixes += nlp.Defaults.prefixes
    prefixes = set(prefixes)
    prefix_re = compile_prefix_regex(prefixes)
    nlp.tokenizer.suffix_search = prefix_re.search


def append_suffix_regex(nlp: Language, suffixes: Optional[List[str]] = None):
    """Append to the breaking prefix rules."""
    suffixes = suffixes if suffixes else BREAKING
    suffixes += nlp.Defaults.suffixes
    suffixes = set(suffixes)
    suffix_re = compile_suffix_regex(suffixes)
    nlp.tokenizer.suffix_search = suffix_re.search


def append_infix_regex(nlp: Language, infixes: Optional[List[str]] = None):
    """Append to the breaking prefix rules."""
    infixes = infixes if infixes else INFIX
    infixes += nlp.Defaults.infixes
    infixes = set(infixes)
    infix_re = compile_infix_regex(infixes)
    nlp.tokenizer.infix_finditer = infix_re.finditer


def append_tokenizer_regex(
        nlp: Language,
        prefixes: Optional[List[str]] = None,
        infixes: Optional[List[str]] = None,
        suffixes: Optional[List[str]] = None
):
    """Append all three prefix, infix, suffix."""
    append_prefix_regex(nlp, prefixes)
    append_infix_regex(nlp, infixes)
    append_suffix_regex(nlp, suffixes)
