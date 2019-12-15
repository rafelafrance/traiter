"""Parse sex notations."""

from pylib.stacked_regex.rule_catalog import RuleCatalog
from pylib.vertnet.parsers.base import Base, convert
import pylib.vertnet.shared_patterns as patterns


CATALOG = RuleCatalog(patterns.CATALOG)


SEX = Base(
    name=__name__.split('.')[-1],
    rules=[
        # JSON keys for sex
        CATALOG.term('json_key', 'sex'),

        # The sexes
        CATALOG.term('intrinsic', 'females? males?'.split()),

        # These are words that indicate that "sex" is not a key
        CATALOG.term('skip', 'and is was'.split()),

        # Allow arbitrary words in some cases
        CATALOG.part('word', r' \b [a-z] [^;,"=:\s]* '),

        # Some patterns need a terminator
        CATALOG.part('separator', ' [;,"] | $ '),

        # E.g.: sex might be female;
        CATALOG.producer(convert, [
            """json_key
                (?P<value> ( intrinsic | word ){1,2} quest? )
                separator"""]),

        # E.g.: sex=female?
        # Or:   sex=unknown
        CATALOG.producer(convert, [
            'json_key (?P<value> ( intrinsic | word ) quest? )']),

        # E.g.: male
        # Or:   male?
        CATALOG.producer(convert, '(?P<value> intrinsic quest? )'),
    ],
)
