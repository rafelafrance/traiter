"""Parse ovaries state notations."""

import re
from lib.trait import Trait
from lib.trait_builders.base_trait_builder import BaseTraitBuilder
from lib.shared_tokens import SharedTokens
from lib.shared_repoduction_tokens import ReproductiveTokens
import lib.writers.csv_formatters.ovaries_state_csv_formatter as \
    ovaries_state_csv_formatter


class OvariesStateTraitBuilder(BaseTraitBuilder):
    """Parser logic."""

    csv_formatter = ovaries_state_csv_formatter.csv_formatter

    def build_token_rules(self):
        """Define the tokens."""
        tkn = SharedTokens()
        r_tkn = ReproductiveTokens()

        self.copy(r_tkn['ovary'])
        self.copy(r_tkn['size'])
        self.copy(r_tkn['uterus'])
        self.copy(r_tkn['fallopian'])
        self.copy(r_tkn['mature'])
        self.copy(r_tkn['active'])
        self.copy(r_tkn['non'])
        self.copy(r_tkn['visible'])
        self.copy(r_tkn['destroyed'])
        self.copy(r_tkn['developed'])
        self.copy(r_tkn['count'])
        self.copy(r_tkn['horns'])
        self.copy(r_tkn['covered'])
        self.copy(r_tkn['fat'])
        self.copy(r_tkn['lut'])
        self.copy(r_tkn['corpus'])
        self.copy(r_tkn['alb'])
        self.copy(r_tkn['nipple'])
        self.copy(tkn['side'])
        self.copy(tkn['cyst'])
        self.copy(r_tkn['color'])
        self.copy(r_tkn['texture'])
        self.copy(r_tkn['sign'])
        self.copy(r_tkn['and'])
        self.copy(tkn['cross'])
        self.copy(tkn['len_units'])

        # Skip words
        self.keyword('skip', ' womb ')

        self.fragment('sep', r' [;] ')

        # We allow random words in some situations
        self.fragment('word', r'[a-z] \w*')

    def build_replace_rules(self):
        """Define rules for token simplification."""
        # E.g.: ovaries and uterine horns
        # Or:   ovaries and fallopian tubes
        self.replace('ovaries', r"""
            ovary ( ( ( and )? uterus ( horns )? )
                    | ( and )? fallopian )?
            """)

        # E.g.: covered in copious fat
        self.replace('coverage', ' covered (word){0,2} fat ')

        # E.g.: +corpus luteum
        self.replace('luteum', ' ( sign )? ( corpus )? (alb | lut) ')

        # E.g.: active
        # Or:   immature
        self.replace(
            'state',
            r"""(non)? ( active | mature | destroyed | visible | developed )""")

        # Skip nipple notation
        self.replace('nips', 'nipple ( size | state )')

        # E.g.: 6 x 4 mm
        self.replace('measurement', [
            'cross len_units',
            'len_units cross',
            'cross'])

    def build_product_rules(self):
        """Define rules for output."""
        # Get left and right side measurements
        # E.g.: ovaries: R 2 c. alb, L sev c. alb
        self.product(self.double, r"""
            ovaries
                (?P<side_a> side)
                    (measurement | count)? (?P<value_a> (word)? luteum)
                (?P<side_b> side)
                    (measurement | count)? (?P<value_b> (word)? luteum)
            """)

        # Typical ovary notation
        self.product(self.convert, [

            # One side may be reported
            # E.g.: left ovary=3x1.5mm, pale pink in color
            """(side)? ovaries
                (measurement)?
                (?P<value>
                    ( word | color | texture | luteum | state | size | and
                        | cyst ){0,3}
                    ( color | texture | luteum | state | size | cyst
                        | fallopian ))
            """,

            # Has the maturity but is possibly missing the size
            'ovaries (side)? (?P<value> (word){0,3} (size | state | luteum))',

            # E.g.: large ovaries
            '(?P<value> (size | state | count){1,3} ) ovaries',

            # E.g.: ovaries and uterine horns covered with copious fat
            'ovaries (?P<value> coverage)',

            # E.g.: reproductive data=Ovary, fallopian tubes dark red
            'ovaries (?P<value> color | texture )',

            # E.g.: +corp. alb both ovaries
            '(?P<value> luteum) (side)? ovaries',

            # E.g.: ovaries L +lut
            'ovaries (side)? luteum',

            # E.g.: 4 bodies in L ovary
            '(?P<value> cyst ) (side)? ovaries',

            # E.g.: corpus luteum visible in both ovaries
            """(?P<value> luteum (state)? )
                (word | len_units){0,3} (side)? ovaries
            """])

    @staticmethod
    def convert(token):
        """Convert parsed token into a trait."""
        value = token.groups['value'].lower()
        if re.match(r'^[\s\d]+$', value):
            return None
        trait = Trait(
            value=value,
            start=token.start,
            end=token.end)
        trait.is_flag_in_token('ambiguous_key', token)
        trait.is_value_in_token('side', token)
        return trait

    @staticmethod
    def double(token):
        """Convert a single token into two traits."""
        trait1 = Trait(
            value=token.groups['value_a'].lower(),
            side=token.groups['side_a'].lower(),
            start=token.start,
            end=token.end)

        trait2 = Trait(
            value=token.groups['value_b'].lower(),
            side=token.groups['side_b'].lower(),
            start=token.start,
            end=token.end)

        return [trait1, trait2]

    @staticmethod
    def should_skip(data, trait):
        """Check if this record should be skipped because of other fields."""
        if not data['sex'] or data['sex'][0].value != 'male':
            return False
        if data[trait]:
            data[trait].skipped = "Skipped because sex is 'male'"
        return True

    @staticmethod
    def adjust_record(data, trait):
        """
        Adjust the trait based on other fields.

        If this is definitely a female then don't flag "gonads" as ambiguous.
        """
        if not data['sex'] or data['sex'][0].value != 'female':
            return
        for parse in data[trait]:
            parse.ambiguous_key = False
