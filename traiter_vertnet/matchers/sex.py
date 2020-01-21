"""Rule-based parsing of sex notations."""

from traiter_shared import DotDict


C = DotDict(
    rule_path='',

    # These should go into a shared module
    key_sep=list('=:"'),    # Separates key from value
    value_sep=list(';,"'),  # Separate value from next key
    quest=list('?'),
    quote=list('"'),
    letters_re='^[a-z]+$',
)


def setup():
    """Build a the rules and attach them to the nlp engine."""
