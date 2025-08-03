from spacy.tokens import Span, Token


def add_extensions():
    if not Span.has_extension("trait"):
        Token.set_extension("flag", default="")
        Token.set_extension("trait", default=None)

        Span.set_extension("trait", default=None)
