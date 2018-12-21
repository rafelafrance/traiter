"""Lex sex annotations."""

from lib.lexers.lex_base import LexBase
import lib.lexers.shared_regexp as regexp


class LexSex(LexBase):
    """Lex testes state annotations."""

    def rule_list(self) -> regexp.Regexps:
        """Define the lexer."""
        return [
            regexp.sep,

            regexp.Regexp('key', regexp.boundary(r' sex ')),

            regexp.Regexp('sex', regexp.boundary(r' males? | females? ')),

            regexp.Regexp('quest', r' \? '),

            # These are words that indicate "sex" is not a key
            regexp.Regexp('skip', regexp.boundary(r' and | is | was ')),

            regexp.word,
        ]
