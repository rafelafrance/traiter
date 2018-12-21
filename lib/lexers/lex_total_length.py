"""Lex total length annotations."""

# pylint: disable=too-few-public-methods,missing-docstring,duplicate-code

from lib.lexers.lex_base import LexBase
import lib.lexers.shared_regexp as regexp


class LexTotalLength(LexBase):
    """Lex total length annotations."""

    def rule_list(self) -> regexp.Regexps:
        return [
            regexp.shorthand,
            regexp.fraction,
            regexp.range,
            regexp.feet,
            regexp.inches,
            regexp.shorthand_key,

            regexp.Regexp('key_with_units', r"""
                total  [\s-]* length [\s-]* in [\s-]* (?: mm | millimeters)
                | length [\s-]* in [\s-]* (?: mm | millimeters)
                | snout [\s-]* vent [\s-]* lengths? [\s-]* in [\s-]*
                    (?: mm | millimeters)
                | head  [\s-]* body [\s-]* length [\s-]* in [\s-]*
                    (?: mm | millimeters)
                """),

            regexp.Regexp('len_key', r"""
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

            regexp.Regexp('ambiguous', regexp.boundary(r"""
                (?<! [\p{Letter}] \s* ) lengths? """)),

            regexp.Regexp('key_units_req', regexp.boundary(
                r""" measurements? | body | total""")),

            regexp.Regexp('stop_plus', r' [.;,] '),

            regexp.metric_len,
            regexp.word,
        ]
