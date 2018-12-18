"""Lex total length annotations."""

# pylint: disable=too-few-public-methods

from lib.lexers.lex_base import LexBase, LexRule, LexRules


class LexTotalLength(LexBase):
    """Lex total length annotations."""

    def rule_list(self) -> LexRules:
        return [
            self.shorthand,
            self.range,
            self.shorthand_key,
            self.feet,
            self.inches,

            LexRule('key_with_units', self.boundary(r"""
                total  [\s-]* length [\s-]* in [\s-]* (?: mm | millimeters)
                | length [\s-]* in [\s-]* (?: mm | millimeters)
                | snout [\s-]* vent [\s-]* lengths? [\s-]* in [\s-]*
                    (?: mm | millimeters)
                | head  [\s-]* body [\s-]* length [\s-]* in [\s-]*
                    (?: mm | millimeters)
                """, right=False)),

            LexRule('total_len_key', self.boundary(r"""
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
                """, right=False)),

            LexRule('ambiguous', self.boundary(r"""
                (?<! [\p{Letter}] \s* ) lengths? """)),

            LexRule('key_units_req', self.boundary(
                r""" measurements? | body | total""")),


            LexRule('stop_plus', r' [.;,] '),

            self.metric_len,
            self.word,
        ]
