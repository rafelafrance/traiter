"""Common functions for custom pipes."""

from typing import Optional, Union

import spacy
from spacy.tokens import Span, Token

REJECT_MATCH = 'reject_match.v1'
TEXT_ACTION = 'text_action.v1'

EntityType = Union[Span, Token]


class RejectMatch(Exception):
    """Raise this when you want to remove a match from doc.ents."""
    pass


@spacy.registry.misc(REJECT_MATCH)
def reject_match(_: Span) -> None:
    """Use this to reject a pattern from doc.ents."""
    raise RejectMatch


@spacy.registry.misc(TEXT_ACTION)
def text_action(ent: EntityType, replace: Optional[dict] = None) -> None:
    """Enrich term matches."""
    text = ent.text.lower()
    label = ent.label_ if isinstance(ent, Span) else ent.ent_type_
    label = ent._.cached_label if ent._.cached_label else label
    ent._.data[label] = text
    if replace:
        words = [replace.get(w, w) for w in text.split()]
        text = ' '.join(words)
        ent._.data[label] = replace.get(text, text)
