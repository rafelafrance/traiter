"""Common actions for enriching matches."""

from spacy.language import Language
from spacy.tokens import Doc

from ..actions import Actions, ActionsType


class ActionPipe:
    """Add data to entities."""

    def __init__(self, actions: ActionsType) -> None:
        self.actions: ActionsType = actions

    def __call__(self, doc: Doc) -> Doc:
        """Perform the assigned action for every entity in the doc."""
        entities = []

        for ent in doc.ents:
            label = f'{ent.label_}_{ent.ent_id_}' if ent.ent_id_ else ent.label_

            action = self.actions.get(label)

            if action == 'remove':
                continue
            elif action:
                action(ent)

            entities.append(ent)

        doc.ents = tuple(entities)
        return doc

    @classmethod
    def add_pipe(
            cls, nlp: Language, actions: Actions, *, name: str = 'actions', **kwargs
    ) -> None:
        """Add an entity ruler to the pipeline."""
        kwargs = {'before': 'parser'} if not kwargs else kwargs
        pipe = cls(actions.actions)
        nlp.add_pipe(pipe, name=name, **kwargs)
