"""Update the tokenizer.

The default Spacy tokenizer works great for model-based parsing but sometimes causes
complicates rule-based parsers.
"""

import re
from typing import List, Optional

import spacy
from spacy.lang.char_classes import (
    ALPHA, ALPHA_LOWER, ALPHA_UPPER, CONCAT_QUOTES, HYPHENS, LIST_ELLIPSES, LIST_ICONS)
from spacy.language import Language

BREAKING = r"""[\[\]\\/()<>˂˃:;,.?"“”'’×+~-]"""

# These rules were useful in the past.
INFIX = LIST_ELLIPSES + LIST_ICONS + [
    r'(?<=[0-9])[+\-\*^](?=[0-9])',
    r'(?<=[{al}{q}])\.(?=[{au}{q}])'.format(
        al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES),
    r'(?<=[{a}]),(?=[{a}])'.format(a=ALPHA),
    r'(?<=[{a}0-9])[:<>=/+](?=[{a}])'.format(a=ALPHA),
    r"""(?:{h})+""".format(h=HYPHENS),
    r"""[\\\[\]\(\)/:;’'“”'+]""",
    r'(?<=[0-9])\.?(?=[{a}])'.format(a=ALPHA),  # 1.word or 1N
    r'(?<=[{a}]),(?=[0-9])'.format(a=ALPHA),  # word,digits
]


def breaking_prefix(nlp: Language, breaking: Optional[str] = None) -> None:
    """Setup custom tokenizer rule for the breaking prefix punctuation."""
    breaking = breaking if breaking else BREAKING
    prefix = re.compile(f'^{breaking}')
    print(nlp.tokenizer.prefix_search)
    print(nlp.tokenizer.prefix_search.__self__.pattern)
    nlp.tokenizer.prefix_search = prefix.search


def breaking_infix(nlp, breaking: Optional[List[str]]) -> None:
    """Setup custom tokenizer rule for the breaking infix rules."""
    breaking = breaking if breaking else INFIX
    infix_regex = spacy.util.compile_infix_regex(breaking)
    nlp.tokenizer.infix_finditer = infix_regex.finditer


def breaking_suffix(nlp: Language, breaking: Optional[str] = None) -> None:
    """Setup custom tokenizer rule for the breaking suffix punctuation."""
    breaking = breaking if breaking else BREAKING
    suffix = re.compile(f'{breaking}$')
    print(nlp.tokenizer.suffix_search)
    print(nlp.tokenizer.suffix_search.__self__.pattern)
    nlp.tokenizer.suffix_search = suffix.search
