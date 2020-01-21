"""Find taxon notations on herbarium specimen labels."""

import pandas as pd
from traiter_shared.trait import Trait
from traiter_shared import patterns
from traiter_shared import util
from traiter.vocabulary import Vocabulary, LOWEST
from traiter_label_babel.parsers.base import Base

PLANT_FAMILIES = util.DATA_DIR / 'itis_plant_families.csv'
PLANT_GENERA = util.DATA_DIR / 'itis_plant_genera.csv'

VOCAB = Vocabulary(patterns.VOCAB)
VOCAB.part('word', r' \S+ ', capture=False, priority=LOWEST)

DATA = pd.read_csv(PLANT_FAMILIES, na_filter=False, dtype=str)
VOCAB.term('plant_family', DATA['complete_name'].tolist())

DATA = pd.read_csv(PLANT_GENERA, na_filter=False, dtype=str)
VOCAB.term('plant_genus', DATA['complete_name'].tolist())


def convert(token):
    """Normalize a parsed taxon notation"""
    return Trait(start=token.start, end=token.end, value=token.group['value'])


PLANT_TAXON = Base(
    name='plant_taxon',
    rules=[
        VOCAB['eol'],
        VOCAB.producer(convert, f' (?P<value> plant_genus word+ ) ')])

PLANT_FAMILY = Base(
    name='plant_family',
    rules=[VOCAB.producer(convert, f' (?P<value> plant_family ) ')])
