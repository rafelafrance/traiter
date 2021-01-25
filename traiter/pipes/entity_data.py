"""Actions for enriching matches."""

from typing import Callable, Dict, List, Optional

import spacy
from spacy.language import Language
from spacy.tokens import Doc, Span, Token

# Extensions for entity data
if not Span.has_extension('data'):
    Span.set_extension('data', default={})
    Token.set_extension('data', default={})
    Span.set_extension('new_label', default='')
    Token.set_extension('new_label', default='')


class RejectMatch(Exception):
    """Raise this when you want to remove a match from doc.ents."""
    pass


@Language.factory('entity_data')
def entity_data(nlp: Language, name: str, actions: Dict[str, str]):
    """Create a entity data dispatch table."""
    return EntityData(actions)


class EntityData:
    """Perform actions to fill user defined fields etc. for all entities."""

    def __init__(self, actions: Dict[str, str]):
        self.dispatch = {k: self.get_action(v) for k, v in actions.items()}

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        for ent in doc.ents:
            label = f'{ent.label_}.{ent.ent_id_}' if ent.ent_id_ else ent.label_

            action = self.dispatch.get(label)

            if action:
                try:
                    action(ent)
                except RejectMatch:
                    continue

                if new_label := ent._.new_label:
                    span = Span(ent.doc, ent.start, ent.end, label=new_label)
                    span._.data = ent._.data
                    ent = span
                    label = new_label

            ent._.data['trait'] = label.split('.')[0]
            ent._.data['start'] = ent.start_char
            ent._.data['end'] = ent.end_char

            entities.append(ent)

        doc.set_ents(entities)
        return doc

    @staticmethod
    def get_action(action: str) -> Callable:
        """Return an action from the misc registry."""
        return spacy.registry.misc.get(action)

    @staticmethod
    def from_terms(
            terms: List[Dict],
            *,
            actions: Optional[Dict[str, str]] = None,
            default: Optional[str] = None
    ) -> Dict[str, str]:
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
        return actions

    @staticmethod
    def from_matchers(*matchers, default: Optional[str] = None) -> Dict[str, str]:
        """Build rules from matchers.

        Matchers are a list of dicts.
        The dict contains these fields:
            1) A "label" for the match.
            2) An optional "action", a registered function name to run upon a match.
            3) An optional "id".
            4) A list of spacy patterns. Each pattern itself is a list of dicts.
        """
        actions = {}
        for matcher in matchers:
            for rule in matcher:
                if action := rule.get('on_match', default):
                    label = rule['label']
                    actions[label] = action
        return actions


REJECT_MATCH = 'reject_match.v1'


@spacy.registry.misc(REJECT_MATCH)
def reject_match(_: Span) -> None:
    """Use this to reject a pattern from doc.ents."""
    raise RejectMatch


TEXT_ACTION = 'text_action.v1'


@spacy.registry.misc(TEXT_ACTION)
def text_action(ent: Span, replace: Optional[Dict] = None) -> None:
    """Enrich term matches."""
    lower = ent.text.lower()
    ent._.data[ent.label_] = replace.get(lower, lower) if replace else lower


FLAG_ACTION = 'flag_action.v1'


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
#     data = ent._.data
#
#     for token in ent:
#         if not keys:
#             data = {**data, **token._.data}
#         else:
#             update = {k: v for k, v in token._.data.items() if k in keys}
#             data = {**data, **update}
#     ent._.data = data
