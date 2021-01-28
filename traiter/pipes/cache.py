"""Save labels for later analysis."""

from spacy.language import Language
from spacy.tokens import Span, Token


# Extensions for entity actions
if not Span.has_extension('cached_label'):
    Span.set_extension('cached_label', default='')
    Token.set_extension('cached_label', default='')


@Language.component('cache_label')
def cache_label(doc):
    """Save current token label so it can be used after it is replace."""
    for token in doc:
        token._.cached_label = token.ent_type_
    return doc
