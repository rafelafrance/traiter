"""Lex sex annotations."""

from lib.lexers.lex_base import LexBase
from lib.lexers.shared_regexp import Regexp, Regexps, get, boundary


class LexSex(LexBase):
    """Lex testes state annotations."""

    def rule_list(self) -> Regexps:
        """Define the lexer."""
        return [
            get('sep'),

            Regexp('key', boundary(r' sex ')),

            Regexp('sex', boundary(r' males? | females? ')),

            Regexp('quest', r' \? '),

            # These are words that indicate "sex" is not a key
            Regexp('skip', boundary(r' and | is | was ')),

            get('word'),
        ]
