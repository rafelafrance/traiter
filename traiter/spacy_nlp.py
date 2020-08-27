"""A wrapper around spacy so we can use our rule-based parsers."""

import re

import spacy
from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER, \
    CONCAT_QUOTES, HYPHENS, LIST_ELLIPSES, LIST_ICONS
from spacy.tokens import Span, Token

Token.set_extension('data', default={})
Token.set_extension('step', default='')

Span.set_extension('data', default={})
Span.set_extension('step', default='')


def spacy_nlp(lang_model='en_core_web_sm', gpu='prefer'):
    """A single function to build the spacy nlp object for singleton use."""
    if gpu == 'prefer':
        spacy.prefer_gpu()
    elif gpu == 'require':
        spacy.require_gpu()

    nlp = spacy.load(lang_model)

    return nlp


def setup_tokenizer(nlp):
    """Setup custom tokenizer rules for the pipeline."""
    infix = (
            LIST_ELLIPSES
            + LIST_ICONS
            + [
                r"(?<=[0-9])[+\-\*^](?=[0-9])",
                r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
                    al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES),
                r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
                # r"(?<=[{a}])(?:{h})(?=[{a}])".format(a=ALPHA, h=HYPHENS),
                r"(?<=[{a}0-9])[:<>=/+](?=[{a}])".format(a=ALPHA),
                r"""(?:{h})+""".format(h=HYPHENS),
                r"""[\\\[\]\(\)/:;"“”'+]""",
                r"(?<=[0-9])\.?(?=[{a}])".format(a=ALPHA),  # 1.word or 1N
            ])

    infix_regex = spacy.util.compile_infix_regex(infix)
    nlp.tokenizer.infix_finditer = infix_regex.finditer

    breaking = r"""[\[\]\\/()<>:;,.?"“”'+-]"""

    prefix = re.compile(f'^{breaking}')
    nlp.tokenizer.prefix_search = prefix.search

    suffix = re.compile(f'{breaking}$')
    nlp.tokenizer.suffix_search = suffix.search


def to_entities(doc, steps=None):
    """Convert trait tokens into entities."""
    spans = []
    for token in doc:
        if ent_type_ := token.ent_type_:
            if steps and token._.step not in steps:
                continue
            if token._.data.get('_skip'):
                continue
            data = {k: v for k, v in token._.data.items()
                    if not k.startswith('_')}

            span = Span(doc, token.i, token.i + 1, label=ent_type_)

            span._.data = data
            span._.step = token._.step

            spans.append(span)

    doc.ents = spans
