"""Parse testes state notations."""

from pylib.stacked_regex.vocabulary import Vocabulary
from pylib.vertnet.trait import Trait
from pylib.vertnet.parsers.base import Base
import pylib.vertnet.shared_reproductive_patterns as patterns

VOCAB = Vocabulary(patterns.VOCAB)


def convert(token):
    """Convert parsed token into a trait producer."""
    trait = Trait(
        value=token.group['value'].lower(),
        start=token.start, end=token.end)
    trait.is_flag_in_token(token, 'ambiguous_key')
    return trait


TESTES_STATE = Base(
    name=__name__.split('.')[-1],
    rules=[
        # Abbreviations for "testes"
        VOCAB.term('abbrev', 'tes ts tnd td tns ta t'.split()),

        # Abbreviations for "testes state"
        VOCAB.term('state_abbrev', 'ns sc'.split()),

        VOCAB['word'],

        VOCAB.grouper('state', [
            'non fully descended',
            'abdominal non descended',
            'abdominal descended',
            'non descended',
            'fully descended',
            'partially descended',
            'size non descended',
            'size descended',
            'descended',
            'size']),

        # Simplify the testes length so it can be skipped easily
        VOCAB.grouper('length', 'cross len_units?'),

        # A typical testes state notation
        # E.g.: reproductiveData: ts 5x3 fully descended
        VOCAB.producer(convert, [
            """label ( testes | abbrev )? length?
                (?P<value> state | state_abbrev | abdominal | scrotal
                    | non scrotal | other | non testes )"""]),

        # E.g.: reproductive data = nonScrotal
        VOCAB.producer(convert, [
            """label length?
                (?P<value> non testes | non scrotal | scrotal )"""]),

        # E.g.: ts inguinal
        VOCAB.producer(convert, [
            """abbrev length?
                (?P<value> state | abdominal | non scrotal
                    | scrotal | other)"""]),

        # E.g.: testes 5x4 mm pt desc
        VOCAB.producer(convert, [
            """testes ( length )?
                (?P<value>
                    ( state | state_abbrev | abdominal | non scrotal
                        | scrotal | other )
                    ( state | state_abbrev | abdominal | non scrotal
                        | scrotal | other | and ){,3}
                    ( state | state_abbrev | abdominal | non scrotal
                        | scrotal | other )
                )"""]),

        # E.g.: testes 5x4 desc
        VOCAB.producer(convert, [
            """testes length?
                (?P<value> state | state_abbrev | abdominal | non scrotal
                    | scrotal | other )"""]),

        # E.g.: no gonads
        VOCAB.producer(convert, [
            """(?P<value> non ( testes | scrotal | gonads ) | scrotal )"""]),
    ],
)
