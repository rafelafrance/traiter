"""Common functions for entity data old_pipes."""
from typing import Union

from spacy.tokens import Span
from spacy.tokens import Token


EntityPatterns = Union[dict, list[dict]]
DispatchTable = dict[str, str]


def add_extensions():
    """Add extensions for spans and tokens used by entity data old_pipes."""
    if not Span.has_extension("data"):
        Span.set_extension("data", default={})
        Token.set_extension("data", default={})

    if not Span.has_extension("new_label"):
        Span.set_extension("new_label", default="")
        Token.set_extension("new_label", default="")

    if not Span.has_extension("merge"):
        Span.set_extension("merge", default=False)
        Token.set_extension("merge", default=False)

    if not Span.has_extension("cached_label"):
        Span.set_extension("label_stack", default=[])
        Token.set_extension("label_stack", default=[])
        Span.set_extension(
            "cached_label",
            getter=lambda x: x._.label_stack[-1] if x._.label_stack else "",
            setter=lambda x, v: x._.label_stack.append(v),
        )
        Token.set_extension(
            "cached_label",
            getter=lambda x: x._.label_stack[-1] if x._.label_stack else "",
            setter=lambda x, v: x._.label_stack.append(v),
        )
        Span.set_extension(
            "first_label",
            getter=lambda x: x._.label_stack[0] if x._.label_stack else "",
        )
        Token.set_extension(
            "first_label",
            getter=lambda x: x._.label_stack[0] if x._.label_stack else "",
        )


class EntityData:
    """A mix-in class for entity data old_pipes."""

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
            span._.new_label = ""
            ent = span
            if (move := span._.data.get(old_label)) is not None:
                span._.data[label] = move
                del span._.data[old_label]

        return ent, label
