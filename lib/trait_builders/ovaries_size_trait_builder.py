"""Parse ovaries size notations."""

from stacked_regex.token import Token
from lib.numeric_trait import NumericTrait
from lib.trait_builders.numeric_trait_builder import NumericTraitBuilder
from lib.shared_tokens import SharedTokens
from lib.shared_repoduction_tokens import ReproductiveTokens
import lib.writers.csv_formatters.ovaries_size_csv_formatter as \
    ovaries_size_csv_formatter


class OvariesSizeTraitBuilder(NumericTraitBuilder):
    """Parser logic."""

    csv_formatter = ovaries_size_csv_formatter.csv_formatter

    def __init__(self, args=None):
        """Build the trait parser."""
        self.tkn = SharedTokens()
        self.r_tkn = ReproductiveTokens()

        # Used to get compounds traits from a single parse
        self.two_sides = self.compile(
            name='two_sides',
            regexp=f' (?P<two_sides> {self.tkn["side"].pattern} ) ')

        # Used to get compounds traits from a single parse
        self.double_cross = self.compile(
            name='double_cross',
            regexp=f' (?P<double_cross> {self.tkn["cross"].pattern} ) ')

        super().__init__(args)

    def build_token_rules(self):
        """Define the tokens."""
        self.copy(self.tkn['uuid'])  # UUIDs cause problems with numbers

        # A label, like: reproductive data
        self.copy(self.r_tkn['label'])

        # Gonads can be for female or male
        self.fragment('ambiguous_key', r' (?P<ambiguous_key> gonads? ) ')

        # Spellings of ovaries
        self.copy(self.r_tkn['ovary'])

        # Various testes state words that are skipped
        self.copy(self.r_tkn['non'])
        self.copy(self.r_tkn['fully'])
        self.copy(self.r_tkn['partially'])
        self.copy(self.r_tkn['other'])
        self.copy(self.r_tkn['horns'])
        self.copy(self.r_tkn['covered'])
        self.copy(self.r_tkn['fat'])
        self.copy(self.r_tkn['developed'])
        self.copy(self.r_tkn['visible'])
        self.copy(self.r_tkn['destroyed'])
        self.copy(self.r_tkn['mature'])
        self.copy(self.r_tkn['uterus'])
        self.copy(self.r_tkn['fallopian'])
        self.copy(self.r_tkn['active'])

        # Spellings of luteum
        self.copy(self.r_tkn['lut'])

        # Spellings of corpus
        self.copy(self.r_tkn['corpus'])

        # Spellings of albicans
        self.copy(self.r_tkn['alb'])

        # Spellings of nipple
        self.copy(self.r_tkn['nipple'])

        # Side: left or [r]
        self.copy(self.tkn['side'])

        # Side: left or [r]
        self.copy(self.tkn['dim_side'])

        # Dimensions: length or width
        self.copy(self.tkn['dimension'])

        # Length by width, like: 10 x 5
        self.copy(self.tkn['cross'])

        # Units
        self.copy(self.tkn['len_units'])

        # Words that join gonad traits
        self.copy(self.r_tkn['in'])
        self.copy(self.r_tkn['and'])

        # We allow random words in some situations
        self.copy(self.r_tkn['word'])

        # Commas are sometimes separators & other times punctuation
        self.fragment('comma', r'[,]')

        # Some patterns require a separator
        self.copy(self.r_tkn['sep'])

    def build_replace_rules(self):
        """Define rules for token simplification."""
        # A key with units, like: gonadLengthInMM
        self.replace('key_with_units', r"""
            ambiguous_key dimension in (?P<units> len_units )
            """)

        # E.g.: active
        # Or:   immature
        self.replace(
            'state', 'active mature destroyed visible developed'.split())

        # Male or female ambiguous, like: gonadLength1
        self.replace('ambiguous', [

            # E.g.: GonadWidth2
            r' ambiguous_key dim_side',

            # E.g.: LeftGonadLength
            r' side ambiguous_key dimension ',

            # E.g.: Gonad Length
            r' ambiguous_key dimension '])

    def build_product_rules(self):
        """Define rules for output."""
        # These patterns contain measurements to both left & right ovaries
        self.product(self.double, [

            # E.g.: reproductive data: ovaries left 10x5 mm, right 10x6 mm
            """label ovary
                (?P<first> side cross )
                (?P<second> side cross )?""",

            # As above but without the ovaries marker:
            # E.g.: reproductive data: left 10x5 mm, right 10x6 mm
            """label
                (?P<first> side cross )
                (?P<second> side cross )?""",

            # Has side before gonad key
            # E.g.: left ovary: 4 x 2 mm
            """(?P<first> side ovary cross )
                (?P<second> side (ovary)? cross )?""",

            # Has the ovaries marker but is lacking the label
            # E.g.: ovaries left 10x5 mm, right 10x6 mm
            """ovary
                (?P<first> (side)? cross )
                (comma)?
                (?P<second> (side)? cross )?"""])

        # A typical testes size notation
        self.product(self.convert, [

            # E.g.: reproductive data: ovaries 10x5 mm
            'label ovary cross',

            # E.g.: reproductive data: left ovaries 10x5 mm
            'label side ovary cross',

            # E.g.: reproductive data: 10x5 mm
            'label cross',

            # May have a few words between the label and the measurement
            """label ( ovary | state | word | sep ){0,3}
                ( ovary | state ) cross""",

            # Handles: gonadLengthInMM 4x3
            # And:     gonadLength 4x3
            '( key_with_units | ambiguous ) cross',

            # E.g.: gonadLengthInMM 6 x 8
            """( key_with_units | ambiguous )
                ( ovary | state | word | sep ){0,3}
                ( ovary | state ) cross""",

            # Anchored by ovaries but with words between
            """ovary ( state | word | sep ){0,3} state cross""",

            # Anchored by ovaries but with only one word in between
            # E.g.: ovaries scrotal 9mm
            'ovary ( state | word ) cross',

            # E.g.: Ovaries 5 x 3
            'ovary cross'])

    def double(self, token):
        """Convert a single token into multiple (two) trait_builders."""
        if not token.groups.get('second'):
            return self.convert(token)

        # Regex second match groups will overwrite the first match groups
        trait2 = NumericTrait(start=token.start, end=token.end)
        trait2.cross_value(token)
        trait2.is_value_in_token('side', token)

        # We need to re-extract the first match groups
        trait1 = NumericTrait(start=token.start, end=token.end)

        groups = self.double_cross.find_matches(token.groups['first'])
        token1 = Token(groups=groups)
        trait1.cross_value(token1)

        groups = self.two_sides.find_matches(token.groups['first'])
        token1 = Token(groups=groups)
        trait1.is_value_in_token('side', token1)

        return [trait1, trait2]

    @staticmethod
    def convert(token):
        """Convert parsed token into a trait product."""
        if token.groups.get('ambiguous_char') \
                and not token.groups.get('value2'):
            return None
        trait = NumericTrait(start=token.start, end=token.end)
        trait.cross_value(token)
        trait.is_flag_in_token('ambiguous_char', token, rename='ambiguous_key')
        trait.is_flag_in_token('ambiguous_key', token)
        trait.is_value_in_token('dimension', token)
        trait.is_value_in_token('side', token)
        return trait

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

        If this is definitely a male then don't flag "gonads" as ambiguous.
        """
        if not data['sex'] or data['sex'][0].value != 'female':
            return
        for parse in data[trait]:
            parse.ambiguous_key = False
