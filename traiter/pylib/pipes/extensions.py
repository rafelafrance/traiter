from spacy.tokens import Span
from spacy.tokens import Token


def add_extensions():
    Span.set_extension("delete", default=False)
    Span.set_extension("data", default={})
    Token.set_extension("data", default={})
    Token.set_extension("term", default="")
    Token.set_extension("info", default=0)
