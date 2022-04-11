"""Common functions for custom old_pipes."""
from typing import Optional
from typing import Union

import spacy
from spacy.tokens import Span
from spacy.tokens import Token

# ###################################################################################
REJECT_MATCH = "traiter.reject_match.v1"


class RejectMatch(Exception):
    """Raise this when you want to remove a match from doc.ents.

    If you're processing a match and you discover that it really isn't a trait/entity
    then you'd raise this exception so the match would not be included in the
    document's entities.
    """

    pass


@spacy.registry.misc(REJECT_MATCH)
def reject_match(_: Span) -> None:
    """Use this to reject a pattern from doc.ents.

    Sometimes it is easier to search for a pattern that you know you don't want
    rather than writing a bunch of rules to work around a set of bad patterns within
    the normal set of rules.
    """
    raise RejectMatch


# ###################################################################################
TEXT_ACTION = "traiter.text_action.v1"


@spacy.registry.misc(TEXT_ACTION)
def text_action(ent: Union[Span, Token], replace: Optional[dict] = None) -> None:
    """Enrich term matches.

    If all you're doing is adding the text (with light processing) to the trait then
    this canned function may be useful.
    """
    text = ent.text.lower()
    label = ent.label_ if isinstance(ent, Span) else ent.ent_type_
    label = ent._.cached_label if ent._.cached_label else label
    ent._.data[label] = text
    if replace:
        words = [replace.get(w, w) for w in text.split()]
        text = " ".join(words)
        ent._.data[label] = replace.get(text, text)
