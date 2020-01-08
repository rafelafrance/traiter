"""
Find collector notations on herbarium specimen labels.
"""

import regex
from itertools import zip_longest
from pylib.shared import util
from pylib.shared.trait import Trait
from pylib.shared.parsers.us_states import STATE_NAMES
from pylib.shared.parsers import name_parts
from pylib.stacked_regex.rule_catalog import RuleCatalog, LAST
from pylib.label_babel.parsers.base import Base

CATALOG = RuleCatalog(name_parts.CATALOG)

MIN_LEN = 5     # Minimum collector name length


def convert(token):
    """Build a collector trait"""
    names = regex.split(r'\s*(?:and|,)\s*', token.groups.get('col_name'))

    traits = []

    for name, suffix in zip_longest(names, names[1:], fillvalue=''):
        if len(name) < MIN_LEN:
            continue

        trait = Trait(start=token.start, end=token.end)
        trait.col_name = name

        if suffix.lower() in name_parts.SUFFIXES:
            trait.col_name = f'{name} {suffix}'

        if name.lower() not in name_parts.SUFFIXES:
            traits.append(trait)

    if token.groups.get('col_no'):
        traits[0].col_no = token.groups['col_no']

    return util.squash(traits)


COLLECTOR = Base(
    name='collector',
    rules=[
        CATALOG['eol'],
        CATALOG['month_name'],
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

        CATALOG.part('noise', r" [_`‘|\[\]]+ "),
        CATALOG.term('header_key', r' herbarium '.split()),

        CATALOG.term('col_no', r""" [[:alpha:][:digit:]]+ """, when=LAST),

        CATALOG.grouper('collector', """
            ( name_part | initial ){2,} 
            ( name_part | part | initial )* """, capture=False),

        # With a label
        CATALOG.producer(convert, """
            (?<= ^ | eol )
            (?<! other_label comma? name_part? ) (?<! part | col_no )
                noise? col_label noise?
                (?P<col_name> collector 
                    ( ( conj | comma ) collector )* ( comma name_part )? )
                noise?
                ( no_label? col_no )? """),

        # Without a label
        CATALOG.producer(convert, """
            (?<= ^ | eol )
            (?<! other_label noise? name_part? )  (?<! part | col_no )
            noise? col_label? noise?
            (?P<col_name> name_part+ ( ( conj | comma ) collector )* )
            ( no_label? col_no )?
            (?! header_key )
            (?= month_name | col_no | eol | $ ) """),
       ])
