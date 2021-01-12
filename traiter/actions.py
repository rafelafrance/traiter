"""Common actions for enriching matches."""

from typing import Dict, Optional

from spacy.tokens import Span

Data = Optional[Dict]
Replace = Optional[Dict[str, Dict]]
Keys = Optional[set]


def null(*args, **kwargs):
    """Return a null."""
    return


def text_action(span: Span, replace: Replace = None) -> Data:
    """Enrich term matches."""
    label = span.label_.split('.')[0]
    return {label: replace.get(span.lower_, span.lower_)}


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
