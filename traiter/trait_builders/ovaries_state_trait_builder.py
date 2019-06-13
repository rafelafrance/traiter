"""Parse testes state notations."""

from traiter.trait import Trait
from traiter.trait_builders.base_trait_builder import BaseTraitBuilder


class OvariesStateTraitBuilder(BaseTraitBuilder):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        self.build_token_rules()
        self.build_replace_rules()
        self.build_product_rules()

        self.compile_regex()

    def build_token_rules(self):
        # self.keyword('label', r' reproductive .? (data |state | condition) ')

        # Various spellings of ovary
        self.fragment('ovary', r' ( ovary s? | ovaries | ov ) \b ')

        # E.g.: small sized
        self.keyword('size', r"""
            ( enlarged | enlarge | large | small | moderate | mod )      
            ( \s* size d? )?
            """)

        # Various spellings of uterus
        self.keyword('uterus', 'uterus uterine'.split())

        # Various forms of fallopian tubes
        self.keyword('fallopian', r' fallopian ( \s* tubes? )? ')

        # Forms of maturity
        self.keyword('immature', 'immature mature'.split())

        # Words related to ovaries
        self.keyword('horns', 'horns?')
        self.keyword('covered', 'covered')
        self.keyword('fat', 'fat')

        # Spellings of corpus
        self.keyword('corpus', 'corpus corpora corp cor c'.split())

        # Spellings of albicans
        self.keyword('alb', 'albicans alb'.split())

        # Spellings of luteum
        self.keyword('lut', ' luteum lute lut'.split())

        # Side keywords
        self.keyword('side', ' (?P<side> both | left | right | [lr] )')

        # Colors associated with ovaries
        self.keyword('color', r' ( dark | light | pale )? \s* (red | pink) ')

        # Sign for presence or absence
        self.fragment('sign', ' [+-] ')

        # Links ovaries and other related traits
        self.fragment('and', ['and', '[&]'])

        # We allow random words in some situations
        self.fragment('word', r'[a-z]+ \w*')

    def build_replace_rules(self):
        """Define rules for token simplification."""
        # E.g.: ovaries and uterine horns
        # Or:   ovaries and fallopian tubes
        self.replace('ovaries', r"""
            ovary ( ( ( and )? uterus ( horns )? )
                    | ( and )? fallopian )?
            """)

        # E.g.: covered in copious fat
        self.replace('coverage', r' covered (word){0,2} fat ')

        # E.g.: +corpus luteum
        self.replace('luteum', r' ( sign )? ( corpus )? (alb | lut) ')

    def build_product_rules(self):
        """Define rules for output."""
        # Get left and right side measurements
        # E.g.: ovaries: R 2 c. alb, L sev c. alb
        self.product(self.double, r"""
            ovaries (?P<side1> side) (?P<value1> ( word )? luteum)
                    (?P<side2> side) (?P<value2> ( word )? luteum)
            """)

        # Typical ovary notation
        self.product(self.convert, [

            # Only one side is reported
            # E.g.: left ovary=3x1.5mm, pale pink in color
            'side ovaries (word){0,3} (?P<value> color)',

            # Has the size but is possibly missing the maturity
            'ovaries (?P<value> ( size ) ( immature )? )',

            # Has the maturity but is possibly missing the size
            'ovaries (?P<value> ( size )? ( immature ) )',

            # E.g.: ovaries and uterine horns covered with copious fat
            'ovaries (?P<value> coverage)',

            # E.g.: reproductive data=Ovary, fallopian tubes dark red
            'ovaries (?P<value> color)',

            # E.g.: +corp. alb both ovaries
            '(?P<value> luteum) ( side )? ovaries',

            # E.g.: ovaries L +lut
            'ovaries ( side )? luteum',
        ])

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
            value=token.groups['value1'].lower(),
            side=token.groups['side1'].lower(),
            start=token.start,
            end=token.end)

        trait2 = Trait(
            value=token.groups['value2'].lower(),
            side=token.groups['side2'].lower(),
            start=token.start,
            end=token.end)

        return [trait1, trait2]
