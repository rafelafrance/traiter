"""Parse date notations."""

from datetime import date
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from pylib.vertnet.trait import Trait
from pylib.shared import patterns
from pylib.stacked_regex.rule_catalog import RuleCatalog
from pylib.label_babel.parsers.base import Base


CATALOG = RuleCatalog(patterns.CATALOG)


DIGITS = r'(?<! \d ) ( [12]\d{3} | \d{1,2} ) (?! \d )'
SEP = r' [/\s-]+ '


def convert(token):
    """Normalize a parsed date"""
    trait = Trait(start=token.start, end=token.end)
    trait.value = parse(token.groups['value']).date()
    if trait.value > date.today():
        trait.value += relativedelta(years=-100)
        trait.century_adjust = True
    trait.value = trait.value.isoformat()[:10]
    return trait


DATE = Base(
    name=__name__.split('.')[-1],
    rules=[
        CATALOG['uuid'],    # Get rid of these before they're a problem

        CATALOG.term('label', ' date '.split()),

        CATALOG.part('digits', DIGITS, capture=False),

        CATALOG.part('numeric_date', fr"""
            {DIGITS} (?P<sep> {SEP} ) {DIGITS} (?P=sep) {DIGITS} """),

        CATALOG.producer(convert, """
            label? (?P<value> digits month_name digits ) """),

        CATALOG.producer(convert, """
            label? (?P<value> month_name digits digits ) """),

        CATALOG.producer(convert, """
            label? (?P<value> numeric_date ) """),

    ],

)
