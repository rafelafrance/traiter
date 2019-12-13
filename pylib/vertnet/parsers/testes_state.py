"""Parse testes state notations."""

from pylib.stacked_regex.rule import term, producer, grouper
from pylib.vertnet.trait import Trait
from pylib.vertnet.parsers.base import Base
from pylib.vertnet.shared_reproductive_patterns import RULE


def convert(token):
    """Convert parsed token into a trait producer."""
    trait = Trait(
        value=token.groups['value'].lower(),
        start=token.start, end=token.end)
    trait.is_flag_in_token(token, 'ambiguous_key')
    return trait


TESTES_STATE = Base(
    name=__name__.split('.')[-1],
    rules=[
        # A label, like: "reproductive data"
        RULE['label'],

        # Spellings of "testes"
        RULE['testes'],

        # "Fully" or "incompletely"
        RULE['fully'],

        # Negation: "non", "not", etc.
        RULE['non'],

        # "Descended"
        RULE['descended'],

        # Abbreviations for "testes"
        term('abbrev', 'tes ts tnd td tns ta t'.split()),

        # Spellings of "scrotum"
        RULE['scrotal'],

        # Spellings of "partially"
        RULE['partially'],

        # Abbreviations for "testes state"
        term('state_abbrev', 'ns sc'.split()),

        # Spellings of "abdominal"
        RULE['abdominal'],

        # Various size words
        RULE['size'],

        # Spellings of "gonads"
        RULE['gonads'],

        # Other state words
        RULE['other'],

        # We will skip over testes size measurements
        RULE['cross'],

        RULE['and'],

        # We allow random words in some situations
        RULE['word'],

        grouper('state', [
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
        grouper('length', 'cross len_units?'),

        # A typical testes state notation
        # E.g.: reproductiveData: ts 5x3 fully descended
        producer(convert, [
            """label ( testes | abbrev )? length?
                (?P<value> state | state_abbrev | abdominal | scrotal
                    | non scrotal | other | non testes )"""]),

        # E.g.: reproductive data = nonScrotal
        producer(convert, [
            """label length?
                (?P<value> non testes | non scrotal | scrotal )"""]),

        # E.g.: ts inguinal
        producer(convert, [
            """abbrev length?
                (?P<value> state | abdominal | non scrotal
                    | scrotal | other)"""]),

        # E.g.: testes 5x4 mm pt desc
        producer(convert, [
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
        producer(convert, [
            """testes length?
                (?P<value> state | state_abbrev | abdominal | non scrotal
                    | scrotal | other )"""]),

        # E.g.: no gonads
        producer(convert, [
            """(?P<value> non ( testes | scrotal | gonads ) | scrotal )"""]),
    ],
)
