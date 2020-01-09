"""
Find taxon notations on herbarium specimen labels.
"""

import pandas as pd
from pylib.shared.trait import Trait
from pylib.shared import patterns
from pylib.shared import util
from pylib.stacked_regex.vocabulary import Vocabulary, LAST
from pylib.label_babel.parsers.base import Base

PLANT_FAMILIES = util.DATA_DIR / 'itis_plant_families.csv'
PLANT_GENERA = util.DATA_DIR / 'itis_plant_genera.csv'

VOCAB = Vocabulary(patterns.VOCAB)
VOCAB.part('word', r' \S+ ', capture=False, when=LAST)

DATA = pd.read_csv(PLANT_FAMILIES, na_filter=False, dtype=str)
VOCAB.term('plant_family', DATA['complete_name'].tolist())

DATA = pd.read_csv(PLANT_GENERA, na_filter=False, dtype=str)
VOCAB.term('plant_genus', DATA['complete_name'].tolist())


def convert(token):
    """Normalize a parsed taxon notation"""
    return Trait(start=token.start, end=token.end, value=token.groups['value'])


PLANT_TAXON = Base(
    name='plant_taxon',
    rules=[
        VOCAB['eol'],
        VOCAB.producer(convert, f' (?P<value> plant_genus word+ ) ')])

PLANT_FAMILY = Base(
    name='plant_family',
    rules=[VOCAB.producer(convert, f' (?P<value> plant_family ) ')])
