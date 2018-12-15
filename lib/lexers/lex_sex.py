"""Lex sex annotations."""

# pylint: disable=too-few-public-methods

from lib.lexers.lex_base import LexBase, LexRule
from lib.lexers.util import boundary


class LexSex(LexBase):
    """Lex testes state annotations."""

    tokens = [
        LexBase.stop,  # We don't want to confuse prefix and suffix notation

        LexRule('key', boundary(r' sex ')),

        LexRule('sex', boundary(r' males? | females? ')),

        LexRule('quest', r' \? '),

        # These are words that indicate "sex" is not a key
        LexRule('skip', boundary(r' and | is | was ')),

        LexBase.word]
