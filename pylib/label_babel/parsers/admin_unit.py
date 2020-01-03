"""Parse administrative unit notations."""

from pylib.shared.trait import Trait
from pylib.shared.parsers import us_counties, us_states
from pylib.stacked_regex.rule_catalog import RuleCatalog
from pylib.label_babel.parsers.base import Base

CATALOG = RuleCatalog(us_counties.CATALOG)


def convert(token):
    """Normalize a parsed date"""
    trait = Trait(start=token.start, end=token.end)

    if token.groups.get('us_county'):
        trait.us_county = token.groups['us_county'].title()

    if token.groups.get('us_state'):
        trait.us_state = us_states.normalize_state(token.groups['us_state'])

    return trait


ADMIN_UNIT = Base(
    name=__name__.split('.')[-1],
    rules=[
        CATALOG['eol'],
        CATALOG.term('label', """ co county """.split(), capture=False),

        CATALOG.producer(convert, ' us_state? label us_county '),
        CATALOG.producer(convert, ' us_county label us_state? '),
    ])
