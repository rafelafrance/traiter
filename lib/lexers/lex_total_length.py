"""Lex total length annotations."""

# pylint: disable=too-few-public-methods

from lib.lexers.lex_base import LexBase
from lib.lexers.util import boundary


class LexTotalLength(LexBase):
    """Lex total length annotations."""

    tokens = [
        LexBase.stop,  # We don't want to confuse prefix and suffix notation

        ('key', boundary(r'  ')),

    ]
