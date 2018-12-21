"""Lex total length annotations."""

from lib.lexers.lex_base import LexBase
from lib.lexers.shared_regexp import Regexp, Regexps, get, boundary


class LexBodyMass(LexBase):
    """Lex total length annotations."""

    def rule_list(self) -> Regexps:
        """Define the lexer."""
        return [
            get('shorthand_mass'),
            get('fraction'),
            get('range'),
            get('pounds'),
            get('ounces'),
            get('shorthand_key'),

            Regexp('key_with_units', boundary(
                r""" weightingrams | massingrams """)),

            Regexp('wt_key', boundary(r"""
                (?: (?: body | full | observed | total ) \.? \s* )?
                    (?: weights?
                    | weigh (?: s | ed | ing )
                    | mass
                    | w \.? t s? \.? )
                | body
                """)),

            get('metric_mass'),
        ]
