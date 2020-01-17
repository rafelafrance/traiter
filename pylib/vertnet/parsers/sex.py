"""Parse sex notations."""

from pylib.stacked_regex.vocabulary import Vocabulary
from pylib.vertnet.parsers.base import Base, convert
import pylib.vertnet.shared_patterns as patterns

VOCAB = Vocabulary(patterns.VOCAB)

SEX = Base(
    name=__name__.split('.')[-1],
    rules=[
        # JSON keys for sex
        VOCAB.term('sex_key', 'sex'),

        # The sexes
        VOCAB.term('sex_vocab', 'females? males?'.split()),

        # These are words that indicate that "sex" is not a key
        VOCAB.term('not_sex', 'and is was'.split()),

        # Allow arbitrary words in some cases
        VOCAB.part('word', r' \b [a-z] [^;,"=:\s]* '),

        # Some patterns need a terminator
        VOCAB.part('separator', ' [;,"] | $ '),

        # E.g.: sex might be female;
        VOCAB.producer(convert, [
            """sex_key
                (?P<value> ( sex_vocab | word ){1,2} quest? ) separator"""]),

        # E.g.: sex=female?, Or: sex=unknown
        VOCAB.producer(convert, [
            'sex_key (?P<value> ( sex_vocab | word ) quest? )']),

        # E.g.: male, Or: male?
        VOCAB.producer(convert, '(?P<value> sex_vocab quest? )'),
    ],
)
