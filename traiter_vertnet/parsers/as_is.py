"""Just grab the notations as they are."""

from traiter.token import Token
from traiter.rule import part, producer
from traiter_vertnet.trait import Trait
from traiter_vertnet.parsers.base import Base


def convert(token: Token) -> Trait:
    """Convert parsed token into a trait product."""
    return Trait(
        value=token.group['value'],
        as_is=True,
        start=token.start, end=token.end)


AS_IS = Base(
    name=__name__.split('.')[-1],
    rules=[
        part('data', [
            r' \S .* \S ',  # Strip leading and trailing spaces
            r' \S ']),      # Get a string with a single character
        producer(convert, '(?P<value> data )'),
    ],
)
