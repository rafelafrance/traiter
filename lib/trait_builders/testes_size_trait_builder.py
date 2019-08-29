"""Parse testes size notations."""

from lib.trait_builders.reproductive_trait_builder \
    import MaleTraitBuilder, GonadSizeTraitBuilder
import lib.writers.csv_formatters.testes_size_csv_formatter as \
    testes_size_csv_formatter


class TestesSizeTraitBuilder(GonadSizeTraitBuilder, MaleTraitBuilder):
    """Parser logic."""

    csv_formatter = testes_size_csv_formatter.csv_formatter

    def build_token_rules(self):
        """Define the tokens."""
        self.copy(self.r_tkn['testes'])

        # Note: abbrev differs from the one in the testes_state_trait
        self.keyword('abbrev', 'tes ts tnd td tns ta'.split())

        # The abbreviation key, just: t. This can be a problem.
        self.fragment('char_key', r' \b t (?! [a-z] )')

        self.copy(self.r_tkn['descended'])
        self.copy(self.r_tkn['scrotal'])
        self.copy(self.r_tkn['abdominal'])
        self.copy(self.r_tkn['size'])
        self.copy(self.r_tkn['other'])

        self.copy(self.tkn['uuid'])  # UUIDs cause problems with numeric traits

        GonadSizeTraitBuilder.build_token_rules(self)

    def build_replace_rules(self):
        """Define rules for token simplification."""

        self.replace('state', [
            """(non | partially | fully )? descended """]
                     + """ scrotal abdominal size other """.split())

        # A key with units, like: gonadLengthInMM
        self.replace('key_with_units', r"""
            ambiguous_key dimension in (?P<units> len_units )
            """)

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
        # These patterns contain measurements to both left & right testes
        self.product(self.double, [

            # E.g.: reproductive data: tests left 10x5 mm, right 10x6 mm
            """label ( testes | abbrev | char_key )
                (?P<first> side cross )
                (?P<second> side cross )?""",

            # As above but without the testes marker:
            # E.g.: reproductive data: left 10x5 mm, right 10x6 mm
            """label
                (?P<first> side cross )
                (?P<second> side cross )?""",

            # Has the testes marker but is lacking the label
            # E.g.: testes left 10x5 mm, right 10x6 mm
            """( testes | abbrev | char_key )
                (?P<first> side cross )
                (?P<second> side cross )?"""])

        # A typical testes size notation
        self.product(self.convert, [

            # E.g.: reproductive data: tests 10x5 mm
            'label ( testes | abbrev | char_key ) cross',

            # E.g.: reproductive data: left tests 10x5 mm
            'label side ( testes | abbrev | char_key ) cross',

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
            '(?P<ambiguous_char> char_key ) cross'])
