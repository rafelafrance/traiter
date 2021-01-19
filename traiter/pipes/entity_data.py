"""Common actions for enriching matches.

Warning:
    This component uses a dispatch table for data enrichment. Spacy does not allow this
    without some sort of registry or global use etc.
    TODO I need to fix the hacky workaround.
"""

from typing import Optional

from spacy.language import Language
from spacy.tokens import Span, Token

from ..actions import ActionsType, RejectMatch

# Extensions for entity data
if not Span.has_extension('data'):
    Span.set_extension('data', default={})
    Token.set_extension('data', default={})
    Span.set_extension('new_label', default='')
    Token.set_extension('new_label', default='')


# TODO Change this to use registered functions
ACTIONS: Optional[ActionsType] = None  # HACK


@Language.component('entity_data')
def entity_data(doc):
    """Perform actions to fill user defined fields etc. for all entities."""
    entities = []

    for ent in doc.ents:
        label = f'{ent.label_}.{ent.ent_id_}' if ent.ent_id_ else ent.label_

        action = ACTIONS.get(label)

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

    doc.ents = tuple(entities)
    return doc


# TODO Change this to use registered functions
def set_actions(actions: ActionsType):
    """Set the global actions."""
    global ACTIONS
    ACTIONS = actions
# HACK ^^^^^^
