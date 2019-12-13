"""Parse sex notations."""

from pylib.stacked_regex.rule import part, term, producer
from pylib.vertnet.shared_patterns import RULE
from pylib.vertnet.parsers.base import Base, convert


SEX = Base(
    name=__name__.split('.')[-1],
    rules=[
        # JSON keys for sex
        term('json_key', 'sex'),

        # The sexes
        term('intrinsic', 'females? males?'.split()),

        # To handle a guessed sex
        RULE['quest'],

        # These are words that indicate that "sex" is not a key
        term('skip', 'and is was'.split()),

        # Allow arbitrary words in some cases
        part('word', r' \b [a-z] [^;,"=:\s]* '),

        # Some patterns need a terminator
        part('separator', ' [;,"] | $ '),

        # E.g.: sex might be female;
        producer(convert, [
            """json_key
                (?P<value> ( intrinsic | word ){1,2} quest? )
                separator"""]),

        # E.g.: sex=female?
        # Or:   sex=unknown
        producer(convert, [
            'json_key (?P<value> ( intrinsic | word ) quest? )']),

        # E.g.: male
        # Or:   male?
        producer(convert, '(?P<value> intrinsic quest? )'),
    ],
)
