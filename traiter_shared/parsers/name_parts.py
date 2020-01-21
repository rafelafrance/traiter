"""Patterns for names."""

import pandas as pd
from traiter_shared import util
from traiter_shared import patterns
from traiter.vocabulary import Vocabulary

NAME_CSV = util.DATA_DIR / 'name_parts.csv'

SUFFIXES = 'filho ii iii jr sr'.split()

VOCAB = Vocabulary(patterns.VOCAB)


def build_name_parts():
    """Build name patterns."""
    df = pd.read_csv(NAME_CSV, na_filter=False, dtype=str)
    VOCAB.term('name_part', df['name'].tolist(), capture=False)


build_name_parts()

VOCAB.term('suffix', SUFFIXES)
VOCAB.term('initial', r'[[:alpha:]]')
