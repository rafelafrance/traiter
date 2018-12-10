"""Lex sex annotations."""

# pylint: disable=too-few-public-methods

from lib.lexers.base_lexer import BaseLexer, isolate


class SexLexer(BaseLexer):
    """Lex testes state annotations."""

    tokens = [
        BaseLexer.stop,  # We don't want to confuse prefix and suffix notation

        ('key', isolate(r' sex ')),

        ('sex', isolate(r' males? | females? ')),

        ('quest', r' \? '),

        # These are words that indicate "sex" is not a key
        ('skip', isolate(r' and | is | was ')),

        BaseLexer.word]
