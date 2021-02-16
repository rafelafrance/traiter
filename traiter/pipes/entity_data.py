"""Common functions for entity data pipes."""

from spacy.tokens import Span, Token


def add_extensions():
    """Add extensions for spans and tokens used by entity data pipes."""
    if not Span.has_extension('data'):
        Span.set_extension('data', default={})
        Token.set_extension('data', default={})

    if not Span.has_extension('new_label'):
        Span.set_extension('new_label', default='')
        Token.set_extension('new_label', default='')

    if not Span.has_extension('cached_label'):
        Span.set_extension('cached_label', default='')
        Token.set_extension('cached_label', default='')


class EntityData:
    """A mix-in class for entity data pipes."""

    def __init__(self):
        """Add span and token extensions for entity data."""
        add_extensions()

    @staticmethod
    def relabel_entity(ent, old_label):
        """Relabel an entity.

        We cannot change a label on a span so we have to make a new one.
        """
        label = old_label

        if new_label := ent._.new_label:
            label = new_label
            span = Span(ent.doc, ent.start, ent.end, label=new_label)
            span._.data = ent._.data
            span._.new_label = ''
            ent = span
            if (move := span._.data.get(old_label)) is not None:
                span._.data[label] = move
                del span._.data[old_label]

        return ent, label
