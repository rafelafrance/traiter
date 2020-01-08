"""
Find collector notations on herbarium specimen labels.
"""

import regex
from pylib.shared import util
from pylib.shared.trait import Trait
from pylib.shared.parsers.us_states import STATE_NAMES
from pylib.shared.parsers import name_parts
from pylib.stacked_regex.rule_catalog import RuleCatalog, LAST
from pylib.label_babel.parsers.base import Base

CATALOG = RuleCatalog(name_parts.CATALOG)


def convert(token):
    """Build a collector trait"""
    names = regex.split(r'\s*(?:and|,)\s*', token.groups.get('col_name'))

    traits = []
    for i, name in enumerate(names):
        trait = Trait(start=token.start, end=token.end)
        trait.col_name = name
        if token.groups.get('col_no') and i == 0:
            trait.col_no = token.groups['col_no']
        traits.append(trait)

    return util.squash(traits)


COLLECTOR = Base(
    name='collector',
    rules=[
        CATALOG['eol'],
        STATE_NAMES,

        CATALOG.term('col_label', r"""
            ( collect(or|ed) | coll | col ) ( \s* by )? 
            """, capture=False),

        CATALOG.term(
            'no_label', r""" number no num """.split(), capture=False),

        CATALOG.term('part', r""" [[:alpha:]]+ """, when=LAST, capture=False),

        CATALOG.term('other_label', r"""
            art artist ass assist assistant auth authors?
            cartographer conservator contributor corator curator curatorial
            det determiner dir director
            ecologist editor entomologist expedition explorer extractor
            gardener geographer geologist georeferencer grower
            herbarium horticulturalist
            illustrator
            manager
            naturalist
            preparator
            researcher
            volunteers?
            writer
            """.split(), capture=False),

        CATALOG.term('col_no', r""" [[:alpha:][:digit:]]+ """, when=LAST),

        CATALOG.grouper('collector', """
            name_part{2,} ( name_part | part )* """, capture=False),

        CATALOG.producer(convert, """
            (?<! other_label comma? name_part? )
                col_label? under?
                (?P<col_name> collector ( ( conj | comma ) collector )* )
                ( no_label? col_no )? """),

        CATALOG.producer(convert, """
            (?<= eol | ^ ) (?<! other_label comma? name_part? )
            col_label? under?
            (?P<col_name> name_part )
            ( no_label? col_no )? (?= eol | $ ) """),
       ])
