"""Parse testes size notations."""

from lib.trait import Trait
from lib.parsers.base import Base
import lib.parsers.shared_tokens as tkn


class TestesSize(Base):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        # Build the tokens
        self.kwd('label', r' reproductive .? (?: data | state | condition ) ')

        self.kwd('key_with_units', r"""
            (?P<ambiguous_sex> gonad ) \s* (?P<dimension> length | width ) \s*
                in \s* (?P<units> millimeters | mm )
            """)

        self.kwd('ambiguous', r"""
            (?P<ambiguous_sex> gonad ) \s* (?P<dimension> length | width )
                \s* (?: (?P<side> [12] ) |  )
            | (?P<side> left | right ) \s* (?P<ambiguous_sex> gonad )
                \s* (?P<dimension> length | width )
            | (?P<ambiguous_sex> gonad ) \s* (?P<dimension> length | width )
            """)

        self.kwd('testes', r' testes |  testis | testicles | test ')
        self.kwd('abbrev', r' tes | ts ')
        self.lit('char_key', r' \b t (?! [a-z] )')
        self.kwd('scrotal', r' scrotum | scrotal | scrot | nscr ')
        self.kwd('lr', r' (?P<side> left | right | l | r ) ')
        self.shared_token(tkn.cross)
        self.lit('word', r' [a-z]+ ')
        self.lit('sep', r' [;,] | $ ')

        # Build rules for parsing the trait
        self.product(self.convert, r"""
            label (?: testes | abbrev | char_key ) cross
            | label (?: testes | abbrev | char_key ) lr cross
            | label cross
            | label testes cross
            | label (?: testes | abbrev | scrotal | word | sep | char_key){1,3}
                (?: testes | abbrev | scrotal | char_key ) cross
            | (?: key_with_units | ambiguous ) cross
            | (?: key_with_units | ambiguous )
                (?: testes | abbrev | scrotal | word | sep | char_key ){1,3}
                (?: testes | abbrev | scrotal | char_key ) cross
            | testes (?: abbrev | scrotal | word | sep | char_key ){1,3}
                (?: abbrev | scrotal | char_key ) cross
            | testes (?: abbrev | scrotal | word | char_key ) cross
            | (?: testes | scrotal | abbrev ) cross
            | (?P<ambiguous_char> char_key ) cross
            """)

        self.finish_init()

    def convert(self, token):  # pylint: disable=no-self-use
        """Convert parsed token into a trait product."""
        if token.groups.get('ambiguous_char') \
                and not token.groups.get('value2'):
            return None
        trait = Trait(start=token.start, end=token.end)
        trait.cross_value(token)
        trait.is_flag_in_token('ambiguous_sex', token)
        trait.flag_from_token('dimension', token)
        trait.flag_from_token('side', token)
        return trait
