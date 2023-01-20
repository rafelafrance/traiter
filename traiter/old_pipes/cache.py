"""Save labels for later analysis."""
from spacy.language import Language

from traiter.old_pipes.entity_data import add_extensions

CACHE_LABEL = "traiter_cache_label_v1"

add_extensions()


@Language.component(CACHE_LABEL)
def cache_label(doc):
    """Save current token label, so it can be used after it is replaced."""
    for token in doc:
        token._.cached_label = token.ent_type_
    return doc
