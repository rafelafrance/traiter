"""Parse administrative unit notations."""

from pylib.vertnet.trait import Trait
from pylib.shared import us_counties
from pylib.stacked_regex.rule_catalog import RuleCatalog
from pylib.label_babel.parsers.base import Base


CATALOG = RuleCatalog(us_counties.CATALOG)


def convert(token):
    """Normalize a parsed date"""
    trait = Trait(start=token.start, end=token.end)

    if token.groups.get('us_county'):
        trait.us_county = token.groups['us_county']

    return trait


ADMIN_UNIT = Base(
    name=__name__.split('.')[-1],
    rules=[
        CATALOG.term('label', """ co county """.split(), capture=False),
        CATALOG.producer(convert, ' us_state label us_county '),
        CATALOG.producer(convert, ' us_county label '),
    ])
