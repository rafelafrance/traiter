"""Just grab the notations as they are."""

from stacked_regex.rule import fragment, producer
from pylib.trait import Trait
from pylib.parsers.base import Base


def convert(token):
    """Convert parsed token into a trait product."""
    return Trait(
        value=token.groups['value'],
        as_is=True,
        start=token.start, end=token.end)


AS_IS = Base(
    scanners=[
        fragment('data', [
            r' \S .* \S ',  # Strip leading and trailing spaces
            r' \S '])       # Get a string with a single character
        ],
    replacers=[],
    producers=[
        producer(convert, '(?P<value> data )')
    ],
)
