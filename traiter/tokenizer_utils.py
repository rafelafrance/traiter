"""Update the tokenizer."""

import re

import spacy
from spacy.lang.char_classes import (
    ALPHA, ALPHA_LOWER, ALPHA_UPPER, CONCAT_QUOTES, HYPHENS, LIST_ELLIPSES, LIST_ICONS)


def add_tokenizer(nlp) -> None:
    """Setup custom tokenizer rules for the pipeline.

    The default Spacy tokenizer works great for model-based parsing but sometimes
    causes trouble with rule-based parsers.
    """
    infix = (
            LIST_ELLIPSES
            + LIST_ICONS
            + [
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
    )

    infix_regex = spacy.util.compile_infix_regex(infix)
    nlp.tokenizer.infix_finditer = infix_regex.finditer

    breaking = r"""[\[\]\\/()<>˂˃:;,.?"“”'’×+~-]"""

    prefix = re.compile(f'^{breaking}')
    nlp.tokenizer.prefix_search = prefix.search

    suffix = re.compile(f'{breaking}$')
    nlp.tokenizer.suffix_search = suffix.search
