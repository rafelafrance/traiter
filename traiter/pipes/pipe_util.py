"""Add extensions for spans and tokens used by trait pipes."""
from spacy.tokens import Span
from spacy.tokens import Token


def add_extensions():
    """Add extensions for spans and tokens used by trait pipes."""
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
        Span.set_extension("cached_label", default="")
        Token.set_extension("cached_label", default="")


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
