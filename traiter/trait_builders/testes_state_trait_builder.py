"""Parse testes state notations."""

from traiter.trait import Trait
from traiter.trait_builders.base_trait_builder import BaseTraitBuilder
import traiter.shared_tokens as tkn
import traiter.writers.csv_formatters.testes_state_csv_formatter as \
    testes_state_csv_formatter


class TestesStateTraitBuilder(BaseTraitBuilder):
    """Parser logic."""

    csv_formatter = testes_state_csv_formatter.csv_formatter

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        self.build_token_rules()
        self.build_replace_rules()
        self.build_product_rules()

        self.compile_regex()

    def build_token_rules(self):
        """Define the tokens."""
        # A label, like: reproductive data
        self.keyword('label', 'reproductive .? ( data |state | condition )')

        # Various spellings of testes
        self.fragment(
            'testes', r' ( testes |  testis | testicles? | test ) \b ')

        # Fully or incompletely
        self.keyword('fully', [
            'fully',
            '( in )? complete ( ly )?'])

        # Negation
        self.fragment('non', r' \b ( not | non | no | semi | sub ) ')

        # Descended
        self.keyword('descended', [
            '( un )? ( des?c?end ( ed )?',
            'desc? )'])

        # Abbreviations for testes
        self.keyword('abbrev', 'tes ts tnd td tns ta t'.split())

        # Spellings of scrotum
        self.fragment(
                'scrotal',
                r'( scrotum | scrotal | scrot | nscr | scr) \b')

        # Spellings of partially
        self.fragment('partially', [
            'partially',
            'part',
            r'\b pt \b'])

        # Abbreviations for testes state
        self.keyword('state_abbrev', 'ns sc'.split())

        # Spellings of abdominal
        self.keyword('abdominal', 'abdominal abdomin abdom abd'.split())

        # Various size words
        self.keyword('size', [
            'visible',
            '( en )? large d?',
            'small'])

        # Spellings of gonads
        self.keyword('gonads', ' (?P<ambiguous_key> gonads? ) ')

        # Other state words
        self.keyword(
            'other',
            'cryptorchism cryptorchid monorchism monorchid inguinal'.split())

        # We will skip over testes size measurements
        self.shared_token(tkn.cross)
        self.shared_token(tkn.len_units)

        # Links ovaries and other related traits
        self.fragment('and', ['and', '[&]'])

        # We allow random words in some situations
        self.fragment('word', r' [a-z]+ ')

    def build_replace_rules(self):
        """Define rules for token simplification."""
        # Simplify state to contain various descended and size tokens
        self.replace('state', [
            'non fully descended',
            'abdominal non descended',
            'abdominal descended',
            'non descended',
            'fully descended',
            'partially descended',
            'size non descended',
            'size descended',
            'descended',
            'size'])

        # Simplify the testes length so it can be skipped easily
        self.replace('length', 'cross ( len_units )?')

    def build_product_rules(self):
        """Define rules for output."""
        # A typical testes state notation
        self.product(self.convert, [

            # E.g.: reproductiveData: ts 5x3 fully descended
            """label ( testes | abbrev )? ( length )?
                (?P<value> state | state_abbrev | abdominal | scrotal
                    | non scrotal | other | non testes )""",

            # E.g.: reproductive data = nonScrotal
            """label ( length )?
                (?P<value> non testes | non scrotal | scrotal )""",

            # E.g.: ts inguinal
            """abbrev ( length )?
                (?P<value> state | abdominal | non scrotal 
                    | scrotal | other)""",

            # E.g.: testes 5x4 mm pt desc
            """testes ( length )?
                (?P<value>
                    ( state | state_abbrev | abdominal | non scrotal
                        | scrotal | other )
                    ( state | state_abbrev | abdominal | non scrotal
                        | scrotal | other | and ){,3}
                    ( state | state_abbrev | abdominal | non scrotal
                        | scrotal | other )
                )""",

            # E.g.: testes 5x4 desc
            """testes ( length )?
                (?P<value> state | state_abbrev | abdominal | non scrotal
                    | scrotal | other )""",

            # E.g.: no gonads
            """(?P<value> non ( testes | scrotal | gonads ) | scrotal )"""])

    @staticmethod
    def convert(token):
        """Convert parsed token into a trait product."""
        trait = Trait(
            value=token.groups['value'].lower(),
            start=token.start,
            end=token.end)
        trait.is_flag_in_token('ambiguous_key', token)
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
