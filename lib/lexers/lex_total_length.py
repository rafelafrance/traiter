"""Lex total length annotations."""

# pylint: disable=too-few-public-methods

from lib.lexers.lex_base import LexBase, LexRule, LexRules


class LexTotalLength(LexBase):
    """Lex total length annotations."""

    def rule_list(self) -> LexRules:
        return [
            self.stop,  # Don't confuse prefix and suffix notation

            self.number,

            LexRule('key_with_units', self.boundary(
                r"""
                    total  [\s-]* length [\s-]* in [\s-]* (?: mm | millimeters)
                    | length [\s-]* in [\s-]* (?: mm | millimeters)
                    | snout [\s-]* vent [\s-]* lengths? [\s-]* in [\s-]*
                        (?: mm | millimeters)
                    | head  [\s-]* body [\s-]* length [\s-]* in [\s-]*
                        (?: mm | millimeters)
                """)),

            LexRule('total_len_key', self.boundary(
                r"""
                    total  [\s-]* length [\s-]* in
                    | (?: total | max | standard ) [\s-]* lengths?
                    | meas (?: [a-z]* )? \.? : \s* L
                    | s \.? l \.?
                    | label [\s.]* lengths?
                """)),

            LexRule('svl_len_key', self.boundary(
                r"""
                    s \.? v \.? ( l \.? )?
                    | snout \s+ vent \s+ lengths?
                """)),

            LexRule('len_key_ambiguous', self.boundary(
                r""" lengths? | tag """)),

            LexRule('other_len_key', self.boundary(
                r"""
                    (?: fork | mean | body ) [\s-]* lengths?
                    | Meas \s* : \s* Length \s* \(L\)
                    | t [o.]? l \.? _?
                """)),

            LexRule('len_key_ambiguous', self.boundary(
                r""" lengths? | tag """)),

            LexRule('key_units_req', self.boundary(
                r""" measurements? | body | total""")),

            LexRule('shorthand_words', self.boundary(
                r""" on \s* tag
                    | specimens?
                    | catalog
                    | measurements (?: \s+ [\p{Letter}]+)
                    | tag \s+ \d+ \s* =? (?: male | female)? \s* ,
                    | meas [.,]? (?: \s+ \w+ \. \w+ \. )?
                    | mesurements
                    | Measurementsnt
                """)),

            LexRule(
                'units',
                r""" (?: [cm] [\s.]? m | in | ft ) [\s.]? s? """)

        ]
