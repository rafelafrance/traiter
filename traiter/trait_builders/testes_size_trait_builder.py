"""Parse testes size notations."""

from stacked_regex.token import Token
from traiter.numeric_trait import NumericTrait
from traiter.trait_builders.base_trait_builder import BaseTraitBuilder
import traiter.shared_tokens as tkn
import traiter.writers.csv_formatters.testes_size_csv_formatter as \
    testes_size_csv_formatter


class TestesSizeTraitBuilder(BaseTraitBuilder):
    """Parser logic."""

    csv_formatter = testes_size_csv_formatter.csv_formatter

    # We need to pair the sides with the correct partner
    side_pairs = {'left': 'right', 'right': 'left', '1': '2', '2': '1'}

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        # Side keywords, like: left
        self.side = ' (?P<side> left | right | [lr] ) '

        # Side abbreviation surrounded by brackets, like: [r]
        self.lr_delim = r' [/(\[] \s* (?P<side> [lr] ) \s* [)\]] '

        # Used to get compounds traits from a single parse
        self.double_side = self.compile(
            name='double_sided',
            regexp=f' (?P<double_side> {self.side} | {self.lr_delim} ) ')

        # Used to get compounds traits from a single parse
        self.double_cross = self.compile(
            name='double_crossed',
            regexp=f' (?P<double_cross> {tkn.cross[1]} ) ')

        self.build_token_rules()
        self.build_product_rules()

        self.compile_regex()

    def build_token_rules(self):
        """Define the tokens."""
        self.shared_token(tkn.uuid)  # UUIDs cause problems with numeric traits

        # A label, like: reproductive data
        self.keyword('label', 'reproductive .? ( data | state | condition )')

        # A key with units, like: gonadLengthInMM
        self.keyword('key_with_units', r"""
            (?P<ambiguous_key> gonad ) \s* (?P<dimension> length | width ) \s*
                in \s* (?P<units> millimeters | mm )
            """)

        # Male or female ambiguous, like: gonadLength1
        self.keyword('ambiguous', [

            # E.g.: GonadWidth2
            r"""(?P<ambiguous_key> gonad ) \s* (?P<dimension> length | width )
                \s* ( (?P<side> [12] ) |  )""",

            # E.g.: LeftGonadLength
            r"""(?P<side> left | right ) \s* (?P<ambiguous_key> gonad )
                \s* (?P<dimension> length | width )""",

            # E.g.: Gonad Length
            r'(?P<ambiguous_key> gonad ) \s* (?P<dimension> length | width )',
        ])

        # Various spellings of testes
        self.keyword('testes', 'testes testis testicles? test'.split())

        # Note: abbrev differs from the one in the testes_state_trait
        self.keyword('abbrev', 'tes ts tnd td tns ta'.split())

        # The abbreviation key, just: t. This can be a problem.
        self.fragment('char_key', r' \b t (?! [a-z] )')

        # Various testes state words
        self.keyword('state', [
            r"""(not | non | no | semi | sub | un | partially | part
                | fully | ( in)? complete(ly)? )?
                (des?c?end ( ed)? | desc? )"""]
            + """
                scrotum scrotal scrot nscr scr ns sc
                abdominal abdomin abdom abd
                visible enlarged small
                gonads?
                cryptorchism cryptorchid monorchism monorchid inguinal
            """.split())

        # Side keywords, like: left
        self.keyword('lr', self.side)

        # Side abbreviation surrounded by brackets, like: [r]
        self.fragment('lr_delim', self.lr_delim)

        # Length by width, like: 10 x 5
        self.shared_token(tkn.cross)

        # Links ovaries and other related traits
        self.fragment('and', ['and', '[&]'])

        # We allow random words in some situations
        self.fragment('word', ' [a-z]+ ')

        # Some patterns require a separator
        self.fragment('sep', ' [;] | $ ')

    def build_product_rules(self):
        """Define rules for output."""
        # These patterns contain measurements to both left & right testes
        self.product(self.double, [

            # E.g.: reproductive data: tests left 10x5 mm, right 10x6 mm
            """label ( testes | abbrev | char_key )
                (?P<first> ( lr | lr_delim ) cross )
                (?P<second> ( lr | lr_delim ) cross )?""",

            # As above but without the testes marker:
            # E.g.: reproductive data: left 10x5 mm, right 10x6 mm
            """label
                (?P<first> ( lr | lr_delim ) cross )
                (?P<second> ( lr | lr_delim ) cross )?""",

            # Has the testes marker but is lacking the label
            # E.g.: testes left 10x5 mm, right 10x6 mm
            """( testes | abbrev | char_key )
                (?P<first> ( lr | lr_delim ) cross )
                (?P<second> ( lr | lr_delim ) cross )?""",
        ])

        # A typical testes size notation
        self.product(self.convert, [

            # E.g.: reproductive data: tests 10x5 mm
            'label ( testes | abbrev | char_key ) cross',

            # E.g.: reproductive data: left tests 10x5 mm
            'label ( lr | lr_delim ) ( testes | abbrev | char_key ) cross',

            # E.g.: reproductive data: 10x5 mm
            'label cross',

            # May have a few words between the label and the measurement
            # E.g.: reproductive data=testes not descended - 6 mm
            """label ( testes | abbrev | state | word | sep | char_key){0,3}
                ( testes | abbrev | state | char_key ) cross""",

            # Handles: gonadLengthInMM 4x3
            # And:     gonadLength 4x3
            '( key_with_units | ambiguous ) cross',

            # E.g.: gonadLengthInMM 6 x 8
            """( key_with_units | ambiguous )
                ( testes | abbrev | state | word | sep | char_key ){0,3}
                ( testes | abbrev | state | char_key ) cross""",

            # Anchored by testes but with words between
            # E.g.: testes scrotal; T = 9mm
            """testes ( abbrev | state | word | sep | char_key ){0,3}
                ( abbrev | state | char_key ) cross""",

            # Anchored by testes but with only one word in between
            # E.g.: testes scrotal 9mm
            'testes ( abbrev | state | word | char_key ) cross',

            # E.g.: Testes 5 x 3
            '( testes | state | abbrev ) cross',

            # E.g.: T 5 x 4
            '(?P<ambiguous_char> char_key ) cross',
        ])

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

        groups = self.double_side.find_matches(token.groups['first'])
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
