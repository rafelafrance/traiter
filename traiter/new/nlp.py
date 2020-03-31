"""A wrapper around spacy so we can use our rule-based parsers."""

import regex
import spacy
from spacy.tokens import Doc, Token  # Span
from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER, HYPHENS
from spacy.lang.char_classes import CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS


def canon(token):
    """Lower case the string & remove noise characters."""
    text = token.text.lower()
    if not (token.is_punct or token.like_num):
        text = regex.sub(r'\p{Dash_Punctuation}', '', text)
    return text


def spacy_nlp(ruler):
    """Wrap spacy."""
    spacy.prefer_gpu()

    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

    infixes = (
        LIST_ELLIPSES
        + LIST_ICONS
        + [
            r"(?<=[0-9])[+\-\*^](?=[0-9-])",
            r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
                al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES),
            r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
            r"(?<=[{a}])(?:{h})(?=[{a}])".format(a=ALPHA, h=HYPHENS),
            r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA),
            # Custom interior rules
            r"""[:"=]""",  # for json-like data
            r"(?<=[0-9])\.(?=[{a}])".format(a=ALPHA)])  # 1.word, 2.other
    infix_regex = spacy.util.compile_infix_regex(infixes)
    nlp.tokenizer.infix_finditer = infix_regex.finditer

    nlp.add_pipe(ruler, name='traiter')

    if Token.has_extension('canon'):
        Token.remove_extension('canon')
    # TODO: see if Token.set_extension('canon', default='') is faster
    Token.set_extension('canon', getter=canon)

    if Doc.has_extension('traits'):
        Doc.remove_extension('traits')
    Doc.set_extension('traits', default=[])

    return nlp
