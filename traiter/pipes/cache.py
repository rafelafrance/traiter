"""Save labels for later analysis."""

from spacy.language import Language

from ..pipe_util import add_spacy_extensions

CACHE_LABEL = 'cache_label'

add_spacy_extensions()


@Language.component(CACHE_LABEL)
def cache_label(doc):
    """Save current token label so it can be used after it is replaced."""
    for token in doc:
        token._.cached_label = token.ent_type_
    return doc
