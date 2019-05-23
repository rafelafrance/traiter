"""Parse body mass notations."""

from functools import partial
from traiter.parse import Parse
from traiter.traits.numeric_trait import NumericTrait
import traiter.shared_tokens as tkn


class BodyMassTrait(NumericTrait):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        self._build_token_rules()
        self._build_replace_rules()
        self._build_product_rules()

        self.compile_regex()

    def _build_token_rules(self):
        self.shared_token(tkn.uuid)

        self.kwd('key_with_units', r"""
            (?: weight | mass) \s* in \s* (?P<units> g (?: rams )? | lbs ) """)
        self.lit('key_leader', ' full | observed | total ')
        self.lit('weight', r' weights? | weigh (?: s | ed | ing ) ')
        self.lit('key_with_dots', r' \b w \.? \s? t s? \.? ')
        self.lit('mass', r' mass ')
        self.lit('body', r' body ')
        self.shared_token(tkn.len_units)
        self.shared_token(tkn.metric_mass)
        self.shared_token(tkn.pounds)
        self.shared_token(tkn.ounces)
        self.shared_token(tkn.shorthand_key)
        self.shared_token(tkn.shorthand)
        self.shared_token(tkn.pair)
        self.kwd('other_wt', r"""
            femur | bac u? (?: lum)? | spleen | thymus | kidney
            | testes | testis | ovaries | epid (?: idymis )? """)
        self.kwd('word', r' (?: [a-z] \w* ) ')
        self.lit('semicolon', r' [;] | $ ')
        self.lit('comma', r' [,] | $ ')

    def _build_replace_rules(self):
        self.replace('wt_key', r"""
            (?<! other_wt )
            (?: key_leader weight | key_leader mass
            | body weight | body mass | body
            | weight | mass | key_with_dots )
            """)

    def _build_product_rules(self):
        self.product(self.shorthand, r' shorthand_key shorthand | shorthand ')

        self.product(partial(self.compound, units=['lbs', 'ozs']), r"""
            wt_key (?P<lbs> pair ) pounds (?: comma )? (?P<ozs> pair ) ounces
            | (?P<ambiguous_key>
                (?P<lbs> pair ) pounds (?: comma )?
                (?P<ozs> pair ) ounces )""")

        self.product(self.simple, r"""
            key_with_units pair
            | wt_key (?P<units> metric_mass | pounds | ounces )
                pair (?! len_units )
            | wt_key pair (?P<units> metric_mass | pounds | ounces )
            | shorthand_key pair (?P<units> metric_mass | pounds | ounces )
            | shorthand_key (?P<units> metric_mass | pounds | ounces )
                pair (?! len_units )
            | wt_key pair (?! len_units ) """)

    @staticmethod
    def shorthand(token):
        """Convert a shorthand value like 11-22-33-44:55g."""
        trait = Parse(start=token.start, end=token.end)
        trait.float_value(token.groups.get('shorthand_wt'))
        if not trait.value:
            return None
        trait.convert_value(token.groups.get('shorthand_wt_units'))
        trait.is_flag_in_token('estimated_wt', token, rename='estimated_value')
        trait.is_shorthand = True
        return trait
