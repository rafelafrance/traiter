"""Functions common to most male & female reproductive traits."""

from stacked_regex.token import Token
from pylib.numeric_trait import NumericTrait
from pylib.trait_builders.numeric_trait_builder import NumericTraitBuilder
from pylib.shared_patterns import SharedPatterns
from pylib.shared_reproductive_patterns import ReproductivePatterns


class GonadSizeTraitBuilder(NumericTraitBuilder):
    """Functions common to gonad sizes for both males & females."""
    gonad_product = None

    def __init__(self, args=None):
        """Build the trait parser."""
        self.tkn = SharedPatterns()
        self.r_tkn = ReproductivePatterns()

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
        # A label, like: reproductive data
        self.copy(self.r_tkn['label'])

        # Gonads can be for female or male
        self.fragment('ambiguous_key', r' (?P<ambiguous_key> gonads? ) ')

        self.copy(self.r_tkn['non'])
        self.copy(self.r_tkn['fully'])
        self.copy(self.r_tkn['partially'])

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

        # Some patterns require a separator
        self.copy(self.r_tkn['sep'])

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


class FemaleTraitBuilder:
    """Functions common to female trait builders."""

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


class MaleTraitBuilder:
    """Functions common to male trait builders."""

    @staticmethod
    def should_skip(data, trait):
        """Check if this record should be skipped because of other fields."""
        if not data['sex'] or data['sex'][0].value != 'female':
            return False
        if data[trait]:
            data[trait].skipped = "Skipped because sex is 'female'"
        return True

    @staticmethod
    def adjust_record(data, trait):
        """
        Adjust the trait based on other fields.

        If this is definitely a male then don't flag "gonads" as ambiguous.
        """
        if not data['sex'] or data['sex'][0].value != 'male':
            return
        for parse in data[trait]:
            parse.ambiguous_key = False
