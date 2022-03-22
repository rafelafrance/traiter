"""Save labels for later analysis."""

from spacy.language import Language

from traiter.pipes.pipes import CACHE_LABEL
from traiter.pipes.entity_data import add_extensions


add_extensions()


@Language.component(CACHE_LABEL)
def cache_label(doc):
    """Save current token label so it can be used after it is replaced."""
    for token in doc:
        token._.cached_label = token.ent_type_
    return doc
