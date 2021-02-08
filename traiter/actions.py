"""Common functions for custom pipes."""

from typing import Optional

import spacy
from spacy.tokens import Span, Token

REJECT_MATCH = 'reject_match.v1'
TEXT_ACTION = 'text_action.v1'
FLAG_ACTION = 'flag_action.v1'


class RejectMatch(Exception):
    """Raise this when you want to remove a match from doc.ents."""
    pass


@spacy.registry.misc(REJECT_MATCH)
def reject_match(_: Span) -> None:
    """Use this to reject a pattern from doc.ents."""
    raise RejectMatch


@spacy.registry.misc(TEXT_ACTION)
def text_action(ent: Span, replace: Optional[dict] = None) -> None:
    """Enrich term matches."""
    lower = ent.text.lower()
    ent._.data[ent.label_] = replace.get(lower, lower) if replace else lower


@spacy.registry.misc(FLAG_ACTION)
def flag_action(
        ent: Span, flag: str = 'flag', value: bool = True, tokens_only: bool = False
) -> None:
    """Flag each token in the span and don't group them."""
    ent._.data[flag] = value
    for token in ent:
        token._.data[flag] = value
    if tokens_only:
        raise RejectMatch

# HOIST_ACTION = 'hoist_action.v1'
# @spacy.registry.misc(HOIST_ACTION)
# def hoist_action(ent: Span, keys: Optional[Set] = None) -> None:
#     """Move data from tokens in span up to the current span."""
#     data = {}
#
#     for token in ent:
#         if not keys:
#             data = {**data, **token._.data}
#         else:
#             update = {k: v for k, v in token._.data.items() if k in keys}
#             data = {**data, **update}
#     ent._.data = data
