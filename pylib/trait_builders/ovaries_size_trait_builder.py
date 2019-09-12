"""Parse ovaries size notations."""

from pylib.trait_builders.reproductive_trait_builder \
    import FemaleTraitBuilder, GonadSizeTraitBuilder
import pylib.writers.csv_formatters.ovaries_size_csv_formatter as \
    ovaries_size_csv_formatter


class OvariesSizeTraitBuilder(GonadSizeTraitBuilder, FemaleTraitBuilder):
    """Parser logic."""

    csv_formatter = ovaries_size_csv_formatter.csv_formatter

    def build_token_rules(self):
        """Define the tokens."""
        self.copy(self.r_tkn['ovary'])
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
        self.copy(self.r_tkn['lut'])
        self.copy(self.r_tkn['corpus'])
        self.copy(self.r_tkn['alb'])
        self.copy(self.r_tkn['nipple'])

        # Commas are sometimes separators & other times punctuation
        self.fragment('comma', r'[,]')

        GonadSizeTraitBuilder.build_token_rules(self)

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
