"""Parse testes state notations."""

from lib.parse import Parse
from lib.traits.base_trait import BaseTrait, ordinal
import lib.shared_tokens as tkn


class TestesStateTrait(BaseTrait):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        self._build_token_rules()
        self._build_replace_rules()
        self._build_product_rules()

        self.finish_init()

    def _build_token_rules(self):
        self.kwd('label', r' reproductive .? (?: data |state | condition ) ')
        self.lit('testes', r' (?: testes |  testis | testicles? | test ) \b ')
        self.kwd('fully', r' fully | (:? in )? complete (?: ly)? ')
        self.lit('non', r' \b (?: not | non | no | semi | sub ) ')
        self.kwd('descended', r' (?: un)? (?: des?c?end (?: ed)? | desc? ) ')
        self.kwd('abbrev', r' tes | ts | tnd | td | tns | ta | t ')
        self.lit(
            'scrotal', r' (?: scrotum | scrotal | scrot | nscr | scr) \b ')
        self.lit('partially', r' partially | part | \b pt \b ')
        self.kwd('state_abbrev', r' ns | sc ')
        self.kwd('abdominal', r' abdominal | abdomin | abdom | abd ')
        self.kwd('size', r' visible | (?: en )? larged? | small ')
        self.kwd('gonads', r' (?P<ambiguous_key> gonads? ) ')
        self.kwd(
            'other',
            ' cryptorchism | cryptorchid | monorchism | monorchid | inguinal ')
        self.shared_token(tkn.cross)
        self.shared_token(tkn.len_units)
        self.kwd('and', r' and | & ')
        self.lit('word', r' [a-z]+ ')

    def _build_replace_rules(self):
        self.replace('state', """
            non fully descended | abdominal non descended
            | abdominal descended | non descended | fully descended
            | partially descended | size non descended | size descended
            | descended | size
            """)
        self.replace('length', ' cross (?: len_units )? ')

    def _build_product_rules(self):
        self.product(
            self.convert,
            """label (?: testes | abbrev )? (?: length )?
                (?P<value> state | state_abbrev | abdominal | scrotal
                    | non scrotal | other | non testes )
            | label (?: length )?
                (?P<value> non testes | non scrotal | scrotal )
            | abbrev (?: length )?
                (?P<value> state | abdominal | non scrotal | scrotal | other)
            | testes (?: length )?
                (?P<value>
                    (?: state | state_abbrev | abdominal | non scrotal
                        | scrotal | other )
                    (?: state | state_abbrev | abdominal | non scrotal
                        | scrotal | other | and ){,3}
                    (?: state | state_abbrev | abdominal | non scrotal
                        | scrotal | other )
                )
            | testes (?: length )?
                (?P<value> state | state_abbrev | abdominal | non scrotal
                    | scrotal | other )
            | (?P<value> non (?: testes | scrotal | gonads ) | scrotal )
            """)

    @staticmethod
    def convert(token):
        """Convert parsed token into a trait product."""
        trait = Parse(
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
        # ambs = []
        for parse in parses:
            value = parse.value.lower()
            if value not in values:
                values.append(value)
                # ambs.append(parse.ambiguous_key)

        # for i, (value, amb) in enumerate(zip(values, ambs), 1):
        for i, value in enumerate(values, 1):
            row[f'testes_{i}10:{ordinal(i)}_testes_state'] = value
            # if amb and value not in ('no gonads', ):
            #    row[f'testes_{i}11:{ordinal(i)}_testes_state_ambiguous'] = amb

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
