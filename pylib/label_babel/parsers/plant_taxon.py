"""Find taxon notations on herbarium specimen labels."""

from pylib.shared.trait import Trait
from pylib.shared.parsers import itis_taxa
from pylib.shared import patterns
from pylib.stacked_regex.rule_catalog import RuleCatalog, LAST
from pylib.label_babel.parsers.base import Base


def convert(token):
    """Normalize a parsed taxon notation"""
    return Trait(start=token.start, end=token.end, value=token.groups['value'])


CATALOG = RuleCatalog(patterns.CATALOG)
CATALOG.part('word', r' \S+ ', capture=False, when=LAST)
itis_taxa.build_families(CATALOG)
itis_taxa.build_genera(CATALOG)


PLANT_TAXON = Base(
    name='plant_taxon',
    rules=[
        CATALOG['eol'],
        CATALOG.producer(convert, f' (?P<value> plant_genus word+ ) ')])

PLANT_FAMILY = Base(
    name='plant_family',
    rules=[CATALOG.producer(convert, f' (?P<value> plant_family ) ')])
