"""Parse testes state notations."""

from traiter.trait import Trait
from traiter.trait_builders.base_trait_builder import BaseTraitBuilder
import traiter.shared_tokens as tkn


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
        # Various spellings of ovary
        self.fragment('ovary', r' ( ovary s? | ovaries | ov ) \b ')

        # E.g.: small sized
        self.keyword('size', r"""
            ( enlarged | enlarge | large | small | shrunken | shrunk 
                | moderate | mod | minute )      
            ( \s* size d? )?
            """)

        # Various spellings of uterus
        self.keyword('uterus', 'uterus uterine'.split())

        # Various forms of fallopian tubes
        self.keyword('fallopian', r' fallopian ( \s* tubes? )? ')

        # Forms of maturity
        self.keyword('mature', 'immature mature imm'.split())

        # Forms of active
        self.keyword('active', 'active inactive'.split())

        # Types of visibility
        self.keyword('visible', 'visible invisible hidden prominent'.split())

        # Forms of destroyed
        self.keyword('destroyed', 'destroy(ed)?')

        # Forms of developed
        self.keyword('developed', r"""
            (fully | incompletely | partially | part)? 
            [.\s-]{0,2}
            (developed | undeveloped | devel | undevel | undev)
        """)

        # Ovary count
        self.keyword('count', r"""(only | all | both)? \s* [12]""")

        # Words related to ovaries
        self.keyword('horns', 'horns?')
        self.keyword('covered', 'covered')
        self.keyword('fat', 'fat')

        # Spellings of luteum
        self.keyword('lut', [
            r' c \.? l \.\? '      # Abbreviation for corpus luteum
        ] + 'luteum lute lut'.split())

        # Spellings of corpus
        self.keyword('corpus', 'corpus corpora corp cor c'.split())

        # Spellings of albicans
        self.keyword('alb', 'albicans alb'.split())

        # Side keywords
        self.keyword('side', ' (?P<side> both | left | right | [lr] )')

        # Colors associated with ovaries
        self.keyword('color', r' ( dark | light | pale )? \s* (red | pink) ')

        # Sign for presence or absence
        self.fragment('sign', ' [+-] ')

        # Links ovaries and other related traits
        self.fragment('and', ['and', '[&]'])

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
            'state', 'active mature destroyed visible developed'.split())

        # E.g.: 6 x 4 mm
        self.replace('measurement', [
            'cross len_units',
            'len_units cross',
            'cross',
        ])

    def build_product_rules(self):
        """Define rules for output."""
        # Get left and right side measurements
        # E.g.: ovaries: R 2 c. alb, L sev c. alb
        self.product(self.double, r"""
            ovaries
                (?P<side_a> side) (measurement | count)? (?P<value_a> (word)? 
                luteum)
                (?P<side_b> side) (measurement | count)? (?P<value_b> (word)? 
                luteum)
            """)

        # Typical ovary notation
        self.product(self.convert, [

            # One side may be reported
            # E.g.: left ovary=3x1.5mm, pale pink in color
            """(side)? ovaries
                (measurement)?
                (?P<value>
                    ( word | color | luteum | state | size){0,3}
                    ( color | luteum | state | size ))
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

            # E.g.: corpus luteum visible in both ovaries
            """(?P<value> luteum (state)? )
                (word | len_units){0,3} (side)? ovaries
            """,
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
