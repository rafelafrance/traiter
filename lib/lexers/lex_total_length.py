"""Lex total length annotations."""

from lib.lexers.lex_base import LexBase
from lib.lexers.shared_regexp import Regexp, Regexps, get, boundary


class LexTotalLength(LexBase):
    """Lex total length annotations."""

    def rule_list(self) -> Regexps:
        """Define the lexer."""
        return [
            get('shorthand'),
            get('fraction'),
            get('range'),
            get('feet'),
            get('inches'),
            get('shorthand_key'),

            Regexp('key_with_units', r"""
                total  [\s-]* length [\s-]* in [\s-]* (?: mm | millimeters)
                | length [\s-]* in [\s-]* (?: mm | millimeters)
                | snout [\s-]* vent [\s-]* lengths? [\s-]* in [\s-]*
                    (?: mm | millimeters)
                | head  [\s-]* body [\s-]* length [\s-]* in [\s-]*
                    (?: mm | millimeters)
                """),

            Regexp('len_key', r"""
                total  [\s-]* length [\s-]* in
                | (?: total | max | standard ) [\s-]* lengths?
                | meas (?: [a-z]* )? \.? : \s* L
                | t [o.]? l \.? _?
                | s \.? l \.?
                | label [\s.]* lengths?
                | (?: fork | mean | body ) [\s-]* lengths?
                | Meas \s* : \s* Length \s* \(L\)
                | s \.? v \.? ( l \.? )?
                | snout \s+ vent \s+ lengths?
                """),

            Regexp('ambiguous', boundary(r"""
                (?<! [\p{Letter}] \s* ) lengths? """)),

            Regexp('key_units_req', boundary(
                r""" measurements? | body | total""")),

            Regexp('stop_plus', r' [.;,] '),

            get('metric_len'),
            get('word'),
        ]
