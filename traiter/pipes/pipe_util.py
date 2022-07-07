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

    if not Span.has_extension("cached_label"):
        Span.set_extension("cached_label", default="")
        Token.set_extension("cached_label", default="")

    if not Span.has_extension("delete"):
        Span.set_extension("delete", default=False)
        Token.set_extension("delete", default=False)
