"""Parse testes state notations."""

from pylib.trait import Trait
from stacked_regex.rule import keyword, producer, replacer
from pylib.parsers.base import Base
from pylib.shared_patterns import SHARED
from pylib.shared_reproductive_patterns import REPRODUCTIVE


def convert(token):
    """Convert parsed token into a trait producer."""
    trait = Trait(
        value=token.groups['value'].lower(),
        start=token.start, end=token.end)
    trait.is_flag_in_token('ambiguous_key', token)
    return trait


TESTES_STATE = Base(
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
        replacer('length', 'cross ( len_units )?'),
    ],

    producers=[
        # A typical testes state notation
        producer(convert, [
            # E.g.: reproductiveData: ts 5x3 fully descended
            """label ( testes | abbrev )? ( length )?
                (?P<value> state | state_abbrev | abdominal | scrotal
                    | non scrotal | other | non testes )"""]),

        producer(convert, [
            # E.g.: reproductive data = nonScrotal
            """label ( length )?
                (?P<value> non testes | non scrotal | scrotal )"""]),

        producer(convert, [
            # E.g.: ts inguinal
            """abbrev ( length )?
                (?P<value> state | abdominal | non scrotal
                    | scrotal | other)"""]),

        producer(convert, [
            # E.g.: testes 5x4 mm pt desc
            """testes ( length )?
                (?P<value>
                    ( state | state_abbrev | abdominal | non scrotal
                        | scrotal | other )
                    ( state | state_abbrev | abdominal | non scrotal
                        | scrotal | other | and ){,3}
                    ( state | state_abbrev | abdominal | non scrotal
                        | scrotal | other )
                )"""]),

        producer(convert, [
            # E.g.: testes 5x4 desc
            """testes ( length )?
                (?P<value> state | state_abbrev | abdominal | non scrotal
                    | scrotal | other )"""]),

        producer(convert, [
            # E.g.: no gonads
            """(?P<value> non ( testes | scrotal | gonads ) | scrotal )"""]),
    ],
)
