from spacy.tokens import Span
from spacy.tokens import Token


def add_extensions():
    Span.set_extension("data", default={})
    Span.set_extension("reject", default=False)
    Token.set_extension("term", default="")
    Token.set_extension("cache", default={})
