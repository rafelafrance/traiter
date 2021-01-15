"""Common actions for enriching matches."""

from typing import Callable, Dict, List, Optional, Union

from spacy.tokens import Span

ResultType = Optional[Dict]
ActionsType = Dict[str, Union[Callable, str]]


class RejectMatch(Exception):
    """Raise this when you want to remove a match from doc.ents."""
    pass


class Actions:
    """Add data to entities."""

    def __init__(self, actions: Optional[ActionsType] = None) -> None:
        self.actions = actions if actions else {}

    def __add__(self, other: 'Actions') -> 'Actions':
        self.actions = {**self.actions, **other.actions}
        return self

    @classmethod
    def from_terms(
            cls,
            terms: List[Dict],
            *,
            actions: Optional[ActionsType] = None,
            default: Optional[Callable] = None
    ) -> 'Actions':
        """Add patterns from terms.

        Add a pattern matcher for each term in the list.

        Each term is a dict with at least these three fields:
            1) label: what is the term's hypernym (ex. color)
            2) pattern: the phrase being matched (ex. gray-blue)
            3) attr: what spacy token field are we matching (ex. LOWER)
            ** There may be other fields in the dict but this method does not use them.
        """
        actions = actions if actions else {}
        if default:
            for label in {t['label'] for t in terms}:
                if label not in actions:
                    actions[label] = default
        return cls(actions)

    @classmethod
    def from_matchers(cls, *matchers, default: Optional[Callable] = None) -> 'Actions':
        """Build rules from matchers.

        Matchers are a list of dicts.
        The dict contains these fields:
            1) A "label" for the match.
            2) An optional function "action" used to attach data to the entity.
            3) An "id" used to add extra data to the match.
            4) A list of spacy patterns. Each pattern is its own list.
        """
        actions = {}
        for matcher in matchers:
            for i, rule in enumerate(matcher):
                if action := rule.get('action', default):
                    label = [rule['label'], rule.get('id')]
                    label = '.'.join(k for k in label if k)
                    actions[label] = action

        return cls(actions)


def reject_match(_: Span) -> None:
    """Use this to reject a pattern from doc.ents."""
    raise RejectMatch


def text_action(ent: Span, replace: Optional[Dict] = None) -> None:
    """Enrich term matches."""
    label = ent.label_.split('.')[0]
    ent._.data[label] = replace.get(ent.lower_, ent.lower_) if replace else ent.lower_


# def hoist_action(ent: Span, keys: Optional[Set] = None) -> None:
#     """Move data from tokens in span up to the current span."""
#     data = ent._.data
#
#     for token in ent:
#         if not keys:
#             data = {**data, **token._.data}
#         else:
#             update = {k: v for k, v in token._.data.items() if k in keys}
#             data = {**data, **update}
#     ent._.data = data


def flag_action(
        ent: Span, flag: str = 'flag', value: bool = True, tokens_only: bool = False
) -> None:
    """Flag each token in the span and don't group them."""
    print(ent)
    ent._.data[flag] = value
    for token in ent:
        token._.data[flag] = value
    if tokens_only:
        raise RejectMatch
