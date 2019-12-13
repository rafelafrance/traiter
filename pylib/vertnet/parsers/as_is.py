"""Just grab the notations as they are."""

from pylib.stacked_regex.token import Token
from pylib.stacked_regex.rule import frag, producer
from pylib.vertnet.trait import Trait
from pylib.vertnet.parsers.base import Base


def convert(token: Token) -> Trait:
    """Convert parsed token into a trait product."""
    return Trait(
        value=token.groups['value'],
        as_is=True,
        start=token.start, end=token.end)


AS_IS = Base(
    name=__name__.split('.')[-1],
    rules=[
        frag('data', [
            r' \S .* \S ',  # Strip leading and trailing spaces
            r' \S ']),      # Get a string with a single character
        producer(convert, '(?P<value> data )'),
    ],
)
