"""Parse testes state notations."""

from traiter.trait import Trait
from traiter.trait_builders.base_trait_builder import BaseTraitBuilder, ordinal
import traiter.shared_tokens as tkn


class TestesStateTraitBuilder(BaseTraitBuilder):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        self.build_token_rules()
        self.build_replace_rules()
        self.build_product_rules()

        self.compile_regex()

    def build_token_rules(self):
        """Define the tokens."""
        self.keyword('label', r' reproductive .? ( data |state | condition ) ')
        self.fragment(
                'testes', r' ( testes |  testis | testicles? | test ) \b ')
        self.keyword('fully', r' fully | ( in )? complete ( ly )? ')
        self.fragment('non', r' \b ( not | non | no | semi | sub ) ')
        self.keyword('descended', r' ( un )? ( des?c?end ( ed )? | desc? ) ')
        self.keyword('abbrev', r' tes | ts | tnd | td | tns | ta | t ')
        self.fragment(
            'scrotal', r' ( scrotum | scrotal | scrot | nscr | scr) \b ')
        self.fragment('partially', r' partially | part | \b pt \b ')
        self.keyword('state_abbrev', r' ns | sc ')
        self.keyword('abdominal', r' abdominal | abdomin | abdom | abd ')
        self.keyword('size', r' visible | ( en )? large d? | small ')
        self.keyword('gonads', r' (?P<ambiguous_key> gonads? ) ')
        self.keyword(
            'other',
            ' cryptorchism | cryptorchid | monorchism | monorchid | inguinal ')
        self.shared_token(tkn.cross)
        self.shared_token(tkn.len_units)
        self.keyword('and', r' and | & ')
        self.fragment('word', r' [a-z]+ ')

    def build_replace_rules(self):
        """Define rules for token simplification."""
        self.replace('state', """
            non fully descended | abdominal non descended
            | abdominal descended | non descended | fully descended
            | partially descended | size non descended | size descended
            | descended | size
            """)
        self.replace('length', ' cross ( len_units )? ')

    def build_product_rules(self):
        """Define rules for output."""
        self.product(
            self.convert,
            """label ( testes | abbrev )? ( length )?
                (?P<value> state | state_abbrev | abdominal | scrotal
                    | non scrotal | other | non testes )
            | label ( length )?
                (?P<value> non testes | non scrotal | scrotal )
            | abbrev ( length )?
                (?P<value> state | abdominal | non scrotal | scrotal | other)
            | testes ( length )?
                (?P<value>
                    ( state | state_abbrev | abdominal | non scrotal
                        | scrotal | other )
                    ( state | state_abbrev | abdominal | non scrotal
                        | scrotal | other | and ){,3}
                    ( state | state_abbrev | abdominal | non scrotal
                        | scrotal | other )
                )
            | testes ( length )?
                (?P<value> state | state_abbrev | abdominal | non scrotal
                    | scrotal | other )
            | (?P<value> non ( testes | scrotal | gonads ) | scrotal )
            """)

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
    def csv_formatter(trait, row, parses):
        """Format the trait for CSV output."""
        if not parses:
            return

        values = []
        for parse in parses:
            value = parse.value.lower()
            if value not in values:
                values.append(value)

        for i, value in enumerate(values, 1):
            row[f'testes_{i}10:{ordinal(i)}_testes_state'] = value

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
        """Adjust the trait based on other fields."""
        if not data['sex'] or data['sex'][0].value != 'male':
            return
        for parse in data[trait]:
            parse.ambiguous_key = False
