"""Lex total length annotations."""

# pylint: disable=too-few-public-methods

from lib.lexers.lex_base import LexBase, LexRule, LexRules


class LexTotalLength(LexBase):
    """Lex total length annotations."""

    def defines(self):
        """ These DEFINEs will appear in the lexer's regexs."""
        return [
            self.define_decimal,
        ]

    def rule_list(self) -> LexRules:
        return [
            self.shorthand,
            self.fraction,
            self.range,
            self.feet,
            self.inches,
            self.shorthand_key,

            LexRule('key_with_units', r"""
                total  [\s-]* length [\s-]* in [\s-]* (?: mm | millimeters)
                | length [\s-]* in [\s-]* (?: mm | millimeters)
                | snout [\s-]* vent [\s-]* lengths? [\s-]* in [\s-]*
                    (?: mm | millimeters)
                | head  [\s-]* body [\s-]* length [\s-]* in [\s-]*
                    (?: mm | millimeters)
                """),

            LexRule('total_len_key', r"""
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

            LexRule('ambiguous', self.boundary(r"""
                (?<! [\p{Letter}] \s* ) lengths? """)),

            LexRule('key_units_req', self.boundary(
                r""" measurements? | body | total""")),

            LexRule('stop_plus', r' [.;,] '),

            self.metric_len,
            self.word,
        ]
