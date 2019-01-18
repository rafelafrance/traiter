"""Parse total length notations."""

from functools import partial
from lib.parsers.base import Base
from lib.parsers.numeric_parser_mixin import NumericParserMixIn
import lib.parsers.shared_tokens as tkn


class TotalLength(NumericParserMixIn, Base):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        # Build the tokens
        self.kwd('key_with_units', r"""
            (?: total | snout \s* vent | head \s* body | fork ) \s*
            len (?: gth )? \s* in \s* (?: millimeters | mm )
            """)

        self.lit('key', r"""
            total  [\s-]* length [\s-]* in
            | (?: total | max | standard ) [\s-]* lengths? \b
            | meas [\s*:]? \s* length [\s(]* [l] [)\s:]*
            | meas (?: [a-z]* )? \.? : \s* l
            | t [o.]? l \.? _?
            | s \.? l \.?
            | label [\s.]* lengths? \b
            | (?: fork | mean | body ) [\s-]* lengths? \b
            | s \.? v \.? ( l \.? )?
            | snout [\s-]* vent [\s-]* lengths? \b
            | (?<! \w \s ) \b l (?! [a-z] )
            """)

        self.lit('ambiguous', r'(?<! [a-z] )(?<! [a-z] \s ) lengths? ')
        self.lit('key_units_req', r' measurements? | body | total ')
        self.shared_token(tkn.len_units)
        self.shared_token(tkn.shorthand_key)
        self.shared_token(tkn.shorthand)
        self.shared_token(tkn.fraction)
        self.shared_token(tkn.pair)
        self.kwd('word', r' (?: [a-z] \w* ) ')
        self.lit('sep', r' [;,] | $ ')

        # Build rules for parsing the trait
        self.product(self.fraction, r"""
            key_units_req fraction (?P<units> len_units)
            | key fraction (?P<units> len_units)
            | (?P<ambiguous_key> ambiguous) fraction (?P<units> len_units)
            """)

        self.product(partial(self.compound, units=['ft', 'in']), r"""
            key (?P<ft> pair) len_units (?P<in> pair) len_units
            | (?P<ambiguous_key>(?P<ft> pair) len_units
                (?P<in> pair) len_units)
            """)

        self.product(self.simple, r"""
            (?P<units> key_with_units) pair
            | shorthand_key pair (?P<units> len_units)
            | shorthand_key (?P<units> len_units) pair
            | key_units_req pair (?P<units> len_units)
            | pair (?P<units> len_units) key
            | pair key
            | ambiguous pair (?P<units> len_units) key
            | ambiguous pair key
            | (?P<ambiguous_key> ambiguous) pair (?P<units> len_units)
            | (?P<ambiguous_key> ambiguous) (?P<units> len_units) pair
            | (?P<ambiguous_key> ambiguous) pair
            | key pair (?P<units> len_units)
            | key (?P<units> len_units) pair
            | key pair
            | key (?: word ){1,3} pair (?P<units> len_units)
            | key (?: word ){1,3} pair
            """)

        self.product(
            partial(self.shorthand_length, measurement='shorthand_tl'),
            r' shorthand_key shorthand | key_units_req shorthand | shorthand ')

        self.finish_init()

    def fix_up_trait(self, trait, text):
        """Fix problematic parses."""
        return self.fix_up_inches(trait, text)
