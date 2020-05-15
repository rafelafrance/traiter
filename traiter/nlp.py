"""A wrapper around spacy so we can use our rule-based parsers."""

import re
import spacy
from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER, \
    CONCAT_QUOTES, HYPHENS, LIST_ELLIPSES, LIST_ICONS
from spacy.tokens import Token  # Doc, Span


Token.set_extension('term', default='')
Token.set_extension('code', default='')


def spacy_nlp():
    """A single function to build the spacy nlp object for singleton use."""
    spacy.prefer_gpu()
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

    infix = (
        LIST_ELLIPSES
        + LIST_ICONS
        + [
            r"(?<=[0-9])[+\-\*^](?=[0-9-])",
            r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
                al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES),
            r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
            # r"(?<=[{a}])(?:{h})(?=[{a}])".format(a=ALPHA, h=HYPHENS),
            r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA),

            r"""(?:{h})""".format(h=HYPHENS),
            r"""[/\\\[\]\(\):;"'-]""",
            r"(?<=[0-9])\.(?=[{a}])".format(a=ALPHA),  # 1.word, 2.other
            ])

    infix_regex = spacy.util.compile_infix_regex(infix)
    nlp.tokenizer.infix_finditer = infix_regex.finditer

    breaking = r"""[\[\]\(\):;,."'-]"""

    prefix = re.compile(f'^{breaking}')
    nlp.tokenizer.prefix_search = prefix.search

    suffix = re.compile(f'{breaking}$')
    nlp.tokenizer.suffix_search = suffix.search

    return nlp


NLP = spacy_nlp()
