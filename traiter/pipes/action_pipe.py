"""Common actions for enriching matches."""

from spacy.language import Language
from spacy.tokens import Doc, Span

from ..actions import Actions, ActionsType, RejectMatch


class ActionPipe:
    """Add data to entities."""

    def __init__(self, actions: ActionsType) -> None:
        self.actions: ActionsType = actions

    def __call__(self, doc: Doc) -> Doc:
        """Perform the assigned action for every entity in the doc."""
        entities = []

        for ent in doc.ents:
            label = f'{ent.label_}.{ent.ent_id_}' if ent.ent_id_ else ent.label_

            action = self.actions.get(label)

            if action:
                try:
                    action(ent)
                except RejectMatch:
                    continue

                if ent._.new_label:
                    ent = self.relabel_entity(ent, ent._.new_label)
                    label = ent._.new_label

            ent._.data['trait'] = label.split('.')[0]
            ent._.data['start'] = ent.start_char
            ent._.data['end'] = ent.end_char

            entities.append(ent)

        doc.ents = tuple(entities)
        return doc

    @staticmethod
    def relabel_entity(ent, new_label):
        """Relabel the entity by creating a new one."""
        span = Span(ent.doc, ent.start, ent.end, label=new_label)
        span._.data = ent._.data
        return span

    @classmethod
    def add_pipe(
            cls, nlp: Language, actions: Actions, *, name: str = 'actions', **kwargs
    ) -> None:
        """Add an entity ruler to the pipeline."""
        kwargs = {'before': 'parser'} if not kwargs else kwargs
        pipe = cls(actions.actions)
        nlp.add_pipe(pipe, name=name, **kwargs)
