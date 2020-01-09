"""Parse date notations."""

from datetime import date
from dateutil import parser
from dateutil.relativedelta import relativedelta
import regex
from pylib.vertnet.trait import Trait
from pylib.shared import util
from pylib.shared import patterns
from pylib.stacked_regex.rule_catalog import RuleCatalog, LAST
from pylib.label_babel.parsers.base import Base

CATALOG = RuleCatalog(patterns.CATALOG)


def convert(token):
    """Normalize a parsed date."""
    trait = Trait(start=token.start, end=token.end)

    value = regex.sub(
        r'[^a-z\d]+', '-', token.groups['value'], flags=util.FLAGS)

    if len(value) < 4:
        return None

    try:
        trait.value = parser.parse(value).date()
    except parser.ParserError:
        return None

    if trait.value > date.today():
        trait.value -= relativedelta(years=100)
        trait.century_adjust = True

    trait.value = trait.value.isoformat()[:10]
    return trait


def short_date(token):
    """Normalize a parsed month year notation."""
    trait = convert(token)
    if trait:
        trait.value = trait.value[:-2] + '??'
    return trait


LABEL_DATE = Base(
    name=__name__.split('.')[-1],
    rules=[
        CATALOG['eol'],
        CATALOG['uuid'],  # Get rid of these before they're a problem

        CATALOG.term('label', ' date '.split()),

        CATALOG.part(
            'digits', r'(?<! \d ) ( [12]\d{3} | \d{1,2} ) (?! \d )',
            capture=True),

        CATALOG.part('sep', r' [/_-]+ ', capture=True),

        CATALOG.part('noise', r""" \w+ """, when=LAST, capture=True),

        CATALOG.producer(convert, """
            label? (?P<value> digits sep? month_name sep? digits ) """),

        CATALOG.producer(convert, """
            label? (?P<value> month_name sep? digits sep? digits ) """),

        CATALOG.producer(convert, """
            label? (?P<value> digits sep digits sep digits ) """),

        CATALOG.producer(short_date, f"""
            label? (?P<value> digits sep digits ) """),

        CATALOG.producer(short_date, f"""
            label? (?P<value> month_name sep? digits ) """),

        CATALOG.producer(short_date, f"""
            label? (?P<value> digits sep? month_name ) """),

    ])
