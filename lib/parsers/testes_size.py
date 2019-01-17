"""Tokens for testes size notations."""

from lib.trait import Trait
from lib.parsers.base import Base
import lib.shared_tokens as tkn


class TestesSize(Base):
    """Parser logic."""

    def __init__(self):
        """Build the trait parser."""
        super().__init__()

        # Build the tokens
        self.kwd('label', r' reproductive .? (?: data | state | condition ) ')

        self.kwd('key_with_units', r"""
            (?P<ambiguous_sex> gonad ) \s* (?P<dimension> length | width ) \s*
                in \s* (?P<units> millimeters | mm )
            """)

        self.kwd('ambiguous', r"""
            (?P<ambiguous_sex> gonad ) \s* (?P<dimension> length | width )
                \s* (?: (?P<index> [12] ) |  )
            | (?P<side> left | right ) \s* (?P<ambiguous_sex> gonad )
                \s* (?P<dimension> length | width )
            | (?P<ambiguous_sex> gonad ) \s* (?P<dimension> length | width )
            """)

        self.kwd('testes', r' testes |  testis | testicles | test ')
        self.kwd('abbrev', r' tes | ts | t ')
        self.kwd('scrotal', r' scrotum | scrotal | scrot | nscr ')
        self.shared_token(tkn.cross)
        self.lit('word', r' [a-z]+ ')

        self.product(self.convert, r"""
            label (?: testes | abbrev) cross
            | label cross
            | label testes cross
            | label (?: testes | abbrev | scrotal | word ){1,3} cross
            | (?: key_with_units | ambiguous ) cross
            | (?: key_with_units | ambiguous )
                (?: testes | abbrev | scrotal | word ){1,3} cross
            | testes cross
            | testes (?: abbrev | scrotal | word ){1,3} cross
            | scrotal cross
            """)

        self.finish_init()

    def convert(self, token):  # pylint: disable=no-self-use
        """Convert parsed token into a trait product."""
        trait = Trait(start=token.start, end=token.end)
        trait.cross_value(token)
        trait.is_flag_in_token('ambiguous_sex', token)
        trait.flag_from_token('dimension', token)
        trait.flag_from_token('index', token)
        trait.flag_from_token('side', token)
        return trait
