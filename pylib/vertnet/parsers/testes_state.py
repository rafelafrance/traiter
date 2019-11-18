"""Parse testes state notations."""

from pylib.stacked_regex.rule import keyword, producer, replacer
from pylib.vertnet.trait import Trait
from pylib.vertnet.parsers.base import Base
from pylib.vertnet.shared_patterns import SHARED
from pylib.vertnet.shared_reproductive_patterns import REPRODUCTIVE


def convert(token):
    """Convert parsed token into a trait producer."""
    trait = Trait(
        value=token.groups['value'].lower(),
        start=token.start, end=token.end)
    trait.is_flag_in_token('ambiguous_key', token)
    return trait


TESTES_STATE = Base(
    name=__name__.split('.')[-1],
    scanners=[

        # A label, like: "reproductive data"
        REPRODUCTIVE['label'],

        # Spellings of "testes"
        REPRODUCTIVE['testes'],

        # "Fully" or "incompletely"
        REPRODUCTIVE['fully'],

        # Negation: "non", "not", etc.
        REPRODUCTIVE['non'],

        # "Descended"
        REPRODUCTIVE['descended'],

        # Abbreviations for "testes"
        keyword('abbrev', 'tes ts tnd td tns ta t'.split()),

        # Spellings of "scrotum"
        REPRODUCTIVE['scrotal'],

        # Spellings of "partially"
        REPRODUCTIVE['partially'],

        # Abbreviations for "testes state"
        keyword('state_abbrev', 'ns sc'.split()),

        # Spellings of "abdominal"
        REPRODUCTIVE['abdominal'],

        # Various size words
        REPRODUCTIVE['size'],

        # Spellings of "gonads"
        REPRODUCTIVE['gonads'],

        # Other state words
        REPRODUCTIVE['other'],

        # We will skip over testes size measurements
        SHARED['cross'],
        SHARED['len_units'],

        REPRODUCTIVE['and'],

        # We allow random words in some situations
        REPRODUCTIVE['word'],
    ],

    replacers=[
        replacer('state', [
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
        replacer('length', 'cross len_units?'),
    ],

    producers=[
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
