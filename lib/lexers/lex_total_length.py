"""Lex total length annotations."""

# pylint: disable=too-few-public-methods,missing-docstring,duplicate-code

from lib.lexers.lex_base import LexBase
import lib.lexers.shared_lex_rules as rule
import lib.lexers.shared_utils as util


class LexTotalLength(LexBase):
    """Lex total length annotations."""

    def rule_list(self) -> rule.LexRules:
        return [
            rule.shorthand,
            rule.fraction,
            rule.range,
            rule.feet,
            rule.inches,
            rule.shorthand_key,

            rule.LexRule('key_with_units', r"""
                total  [\s-]* length [\s-]* in [\s-]* (?: mm | millimeters)
                | length [\s-]* in [\s-]* (?: mm | millimeters)
                | snout [\s-]* vent [\s-]* lengths? [\s-]* in [\s-]*
                    (?: mm | millimeters)
                | head  [\s-]* body [\s-]* length [\s-]* in [\s-]*
                    (?: mm | millimeters)
                """),

            rule.LexRule('total_len_key', r"""
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

            rule.LexRule('ambiguous', util.boundary(r"""
                (?<! [\p{Letter}] \s* ) lengths? """)),

            rule.LexRule('key_units_req', util.boundary(
                r""" measurements? | body | total""")),

            rule.LexRule('stop_plus', r' [.;,] '),

            rule.metric_len,
            rule.word,
        ]
