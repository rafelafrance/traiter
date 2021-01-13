"""Common actions for enriching matches."""

from typing import Dict, Optional

from spacy.tokens import Span

Data = Optional[Dict]
OptDict = Optional[Dict[str, Dict]]
Keys = Optional[set]


def forget(*args, **kwargs):
    """Return a null so that matchers will exclude (or forget) the match.

    This is useful for when a phrase that will match a term but is not actually one.
    For instance, it may be normal for the documents to have an unadorned number "4" as
    a count but only if the suffix isn't something like "days". So, "4" is a count but
    "4 days" is not.
    """
    return


def text_action(span: Span, replace: OptDict = None) -> Data:
    """Enrich term matches."""
    label = span.label_.split('.')[0]

    if replace:
        return {label: replace.get(span.lower_, span.lower_)}

    return {label: span.lower_}


def hoist_action(span: Span, keys: Keys = None) -> Data:
    """Move data from tokens in span up to the current span."""
    data = {}

    for token in span:
        if not keys:
            data = {**data, **token._.data}
        else:
            update = {k: v for k, v in token._.data.items() if k in keys}
            data = {**data, **update}

    return data


def flag_action(span: Span, flag: str = 'flag', value: bool = True) -> Data:
    """Flag each token in the span and don't group them."""
    for token in span:
        token._.data[flag] = value
    return
