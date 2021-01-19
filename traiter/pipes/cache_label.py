"""Save labels for later analysis."""

from spacy.language import Language
from spacy.tokens import Span, Token


# Extensions for entity actions
if not Span.has_extension('label_cache'):
    Span.set_extension('label_cache', default='')
    Token.set_extension('label_cache', default='')


@Language.component('cache_label')
def cache_label(doc):
    """Save current token label so it can be used after it is replace."""
    for token in doc:
        token._.label_cache = token.ent_type_
    return doc
