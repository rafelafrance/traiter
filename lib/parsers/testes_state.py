"""Parse testes state notations."""

from lib.trait import Trait
from lib.parsers.base import Base
import lib.parsers.shared_tokens as tkn


class TestesState(Base):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        # Build the tokens
        self.kwd('label', r' reproductive .? (?: data |state | condition ) ')
        self.lit('testes', r' (?: testes |  testis | testicles | test ) \b ')
        self.kwd('fully', r' fully | (:? in ) complete (?: ly) ')
        self.lit('non', r' \b (?: not | non | no | semi | sub) ')
        self.kwd('descended', r' (?: un)? (?: des?c?end (?: ed)? | desc? ) ')
        self.kwd('abbrev', r' tes | ts | t ')
        self.lit(
            'scrotal', r' (?: scrotum | scrotal | scrot | nscr | scr) \b ')
        self.lit('partially', r' partially | part ')
        self.kwd('state_abbrev', r' ns | sc ')
        self.kwd('abdominal', r' abdominal | abdomin | abdom ')
        self.kwd('size', r' visible | enlarged | small ')
        self.kwd('gonads', r' (?P<ambiguous_sex> gonads? ) ')
        self.kwd(
            'other',
            ' cryptorchism | cryptorchid | monorchism | monorchid | inguinal ')
        self.shared_token(tkn.cross)
        self.shared_token(tkn.len_units)
        self.lit('word', r' [a-z]+ ')

        # Build rules for token replacement
        self.replace('state', """
            non fully descended | abdominal non descended
            | abdominal descended | non descended | fully descended
            | partially descended | size non descended | size descended
            | descended | size
            """)
        self.replace('length', ' cross (?: len_units )? ')

        # Build rules for parsing the trait
        self.product(
            self.convert,
            """label (testes | abbrev)? (?: length )?
                (?P<value> state | state_abbrev | abdominal | scrotal
                    | non scrotal | other | non testes )
            | label (?: length )?
                (?P<value> non testes | non scrotal | scrotal )
            | abbrev (?: length )?
                (?P<value> state | abdominal | non scrotal | scrotal | other)
            | testes (?: length )?
                (?P<value> state | state_abbrev | abdominal | non scrotal
                | scrotal | other )
            | (?P<value> non testes | non scrotal | non gonads | scrotal )
            """)

        self.finish_init()

    def convert(self, token):  # pylint: disable=no-self-use
        """Convert parsed token into a trait product."""
        trait = Trait(
            value=token.groups['value'].lower(),
            start=token.start,
            end=token.end)
        trait.is_flag_in_token('ambiguous_sex', token)
        return trait
