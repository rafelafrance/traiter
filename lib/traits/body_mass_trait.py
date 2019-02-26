"""Parse body mass notations."""

from functools import partial
from lib.parse import Parse
from lib.traits.numeric_trait import NumericTrait
import lib.shared_tokens as tkn


class BodyMassTrait(NumericTrait):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        # Build the tokens
        self.kwd('key_with_units', r"""
            (?: weight | mass) \s* in \s* (?P<units> g (?: rams )? ) """)
        self.lit('key_leader', ' full | observed | total ')
        self.lit('weight', r' weights? | weigh (?: s | ed | ing ) ')
        self.lit('key_with_dots', r' \b w \.? \s? t s? \.? ')
        self.lit('mass', r' mass ')
        self.lit('body', r' body ')
        self.shared_token(tkn.mass_units)
        self.shared_token(tkn.shorthand_key)
        self.shared_token(tkn.shorthand)
        self.shared_token(tkn.pair)
        self.kwd('word', r' (?: [a-z] \w* ) ')
        self.lit('sep', r' [;,] | $ ')

        # Build rules for token replacement
        self.replace('wt_key', r"""
            key_leader weight | key_leader mass
            body weight | body mass | body
            | weight | mass | key_with_dots
            """)

        # Build rules for parsing the trait
        self.product(self.shorthand, r' shorthand_key shorthand | shorthand ')

        self.product(partial(self.compound, units=['lbs', 'ozs']), r"""
            wt_key (?P<lbs> pair ) mass_units (?P<ozs> pair ) mass_units
            | (?P<ambiguous_key>
                (?P<lbs> pair ) mass_units (?P<ozs> pair ) mass_units )""")

        self.product(self.simple, r"""
            key_with_units pair
            | wt_key (?P<units> mass_units ) pair
            | wt_key pair (?P<units> mass_units )
            | shorthand_key pair (?P<units> mass_units )
            | shorthand_key (?P<units> mass_units ) pair
            | wt_key pair""")

        self.finish_init()

    def shorthand(self, token):  # pylint: disable=no-self-use
        """Convert a shorthand value like 11-22-33-44:55g."""
        trait = Parse(start=token.start, end=token.end)
        trait.float_value(token.groups.get('shorthand_wt'))
        if not trait.value:
            return None
        trait.convert_value(token.groups.get('shorthand_wt_units'))
        trait.is_flag_in_token('estimated_wt', token, rename='estimated_value')
        return trait
