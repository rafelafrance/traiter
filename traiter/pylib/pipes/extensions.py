from spacy.tokens import Span, Token


def add_extensions():
    if not Span.has_extension("delete"):
        Span.set_extension("trait", default=None)
        Token.set_extension("trait", default=None)

        Token.set_extension("term", default="")

        Token.set_extension("flag", default="")
        Token.set_extension("data", default={})  # ??

        Span.set_extension("data", default={})  # TODO delete me
        Span.set_extension("delete", default=False)  # TODO delete me
        Span.set_extension("relabel", default="")  # TODO delete me
