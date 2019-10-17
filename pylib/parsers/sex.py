"""Parse sex notations."""

from stacked_regex.rule import fragment, keyword, producer
from pylib.parsers.base import Base, convert


SEX = Base(
    scanners=[
        # JSON keys for sex
        keyword('json_key', 'sex'),

        # The sexes
        keyword('intrinsic', 'females? males?'.split()),

        # To handle a guessed sex
        fragment('quest', '[?]'),

        # These are words that indicate that "sex" is not a key
        keyword('skip', 'and is was'.split()),

        # Allow arbitrary words in some cases
        fragment('word', r' \b [a-z] [^;,"=:\s]* '),

        # Some patterns need a terminator
        fragment('separator', ' [;,"] | $ '),
    ],

    replacers=[],

    producers=[
        # E.g.: sex might be female;
        producer(convert, [
            """json_key
                (?P<value> ( intrinsic | word ){1,2} ( quest )? )
                separator"""]),

        # E.g.: sex=female?
        # Or:   sex=unknown
        producer(convert, [
            'json_key (?P<value> ( intrinsic | word ) ( quest )? )']),

        # E.g.: male
        # Or:   male?
        producer(convert, '(?P<value> intrinsic ( quest )? )'),
    ],
)
