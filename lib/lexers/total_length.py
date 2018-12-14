"""Lex total length annotations."""

# pylint: disable=too-few-public-methods

from lib.lexers.base import Base
from lib.lexers.util import boundary


class LexTotalLength(Base):
    """Lex total length annotations."""

    tokens = [
        Base.stop,  # We don't want to confuse prefix and suffix notation

        ('key', boundary(r'  ')),

    ]
