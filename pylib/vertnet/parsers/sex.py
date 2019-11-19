"""Parse sex notations."""

from pylib.stacked_regex.rule import fragment, keyword, producer
from pylib.vertnet.shared_patterns import RULE
from pylib.vertnet.parsers.base import Base, convert


SEX = Base(
    name=__name__.split('.')[-1],
    rules=[
        # JSON keys for sex
        keyword('json_key', 'sex'),

        # The sexes
        keyword('intrinsic', 'females? males?'.split()),

        # To handle a guessed sex
        RULE['quest'],

        # These are words that indicate that "sex" is not a key
        keyword('skip', 'and is was'.split()),

        # Allow arbitrary words in some cases
        fragment('word', r' \b [a-z] [^;,"=:\s]* '),

        # Some patterns need a terminator
        fragment('separator', ' [;,"] | $ '),

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
