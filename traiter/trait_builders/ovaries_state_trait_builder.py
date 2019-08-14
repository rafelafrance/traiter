"""Parse testes state notations."""

from traiter.trait import Trait
from traiter.trait_builders.base_trait_builder import BaseTraitBuilder
import traiter.shared_tokens as tkn
import traiter.shared_repoduction_tokens as r_tkn
import traiter.writers.csv_formatters.ovaries_state_csv_formatter as \
    ovaries_state_csv_formatter


class OvariesStateTraitBuilder(BaseTraitBuilder):
    """Parser logic."""

    csv_formatter = ovaries_state_csv_formatter.csv_formatter

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        self.build_token_rules()
        self.build_replace_rules()
        self.build_product_rules()

        self.compile_regex()

    def build_token_rules(self):
        """Define the tokens."""
        # Spellings of ovary
        self.shared_token(r_tkn.ovary)

        # E.g.: small sized
        self.shared_token(r_tkn.size)

        # Spellings of uterus
        self.shared_token(r_tkn.uterus)

        # Various forms of fallopian tubes
        self.shared_token(r_tkn.fallopian)

        # Forms of "maturity"
        self.shared_token(r_tkn.mature)

        # Forms of "active"
        self.shared_token(r_tkn.active)

        # Types of "visibility"
        self.shared_token(r_tkn.non)

        # Types of "visibility"
        self.shared_token(r_tkn.visible)

        # Forms of "destroyed"
        self.shared_token(r_tkn.destroyed)

        # Forms of "developed"
        self.shared_token(r_tkn.developed)

        # Ovary count
        self.shared_token(r_tkn.count_)

        # Words related to ovaries
        self.shared_token(r_tkn.horns)
        self.shared_token(r_tkn.covered)
        self.shared_token(r_tkn.fat)

        # Spellings of luteum
        self.shared_token(r_tkn.lut)

        # Spellings of corpus
        self.shared_token(r_tkn.corpus)

        # Spellings of albicans
        self.shared_token(r_tkn.alb)

        # Spellings of nipple
        self.shared_token(r_tkn.nipple)

        # Side keywords
        self.shared_token(tkn.side)

        # Colors associated with gonads
        self.shared_token(tkn.cyst)

        # Colors associated with gonads
        self.shared_token(r_tkn.color)

        # Sign for presence or absence
        self.shared_token(r_tkn.sign)

        # Links ovaries and other related traits
        self.shared_token(r_tkn.and_)

        # We will exclude testes measurements
        self.shared_token(tkn.cross)
        self.shared_token(tkn.len_units)

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
                    ( word | color | luteum | state | size | and | cyst ){0,3}
                    ( color | luteum | state | size | cyst ))
            """,

            # Has the maturity but is possibly missing the size
            'ovaries (side)? (?P<value> (word){0,3} (size | state | luteum))',

            # E.g.: large ovaries
            '(?P<value> (size | state | count){1,3} ) ovaries',

            # E.g.: ovaries and uterine horns covered with copious fat
            'ovaries (?P<value> coverage)',

            # E.g.: reproductive data=Ovary, fallopian tubes dark red
            'ovaries (?P<value> color)',

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
        trait = Trait(
            value=token.groups['value'].lower(),
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
