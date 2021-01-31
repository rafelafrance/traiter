"""Save labels for later analysis."""

from spacy.language import Language
from spacy.tokens import Span, Token

CACHE_LABEL = 'cache_label'

if not Span.has_extension('cached_label'):
    Span.set_extension('cached_label', default='')
    Token.set_extension('cached_label', default='')


@Language.component(CACHE_LABEL)
def cache_label(doc):
    """Save current token label so it can be used after it is replaced."""
    for token in doc:
        token._.cached_label = token.ent_type_
    return doc
