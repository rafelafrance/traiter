from spacy.tokens import Span, Token


def add_extensions():
    if not Span.has_extension("delete"):
        Span.set_extension("delete", default=False)
        Span.set_extension("relabel", default="")
        Span.set_extension("data", default={})

        Token.set_extension("data", default={})
        Token.set_extension("term", default="")
        Token.set_extension("flag", default="")
