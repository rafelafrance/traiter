"""Lex sex annotations."""

# pylint: disable=too-few-public-methods

from lib.lexers.base import Base
from lib.lexers.util import boundary


class LexSex(Base):
    """Lex testes state annotations."""

    tokens = [
        Base.stop,  # We don't want to confuse prefix and suffix notation

        ('key', boundary(r' sex ')),

        ('sex', boundary(r' males? | females? ')),

        ('quest', r' \? '),

        # These are words that indicate "sex" is not a key
        ('skip', boundary(r' and | is | was ')),

        Base.word]
