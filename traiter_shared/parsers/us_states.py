"""Patterns for US states."""

import regex
import pandas as pd
from traiter_shared import util
from traiter_shared import patterns
from traiter.vocabulary import Vocabulary

STATE_CSV = util.DATA_DIR / 'US_states.csv'
STATES = {}
STATE_NAMES = []
NORMALIZE_US_STATE = {}

VOCAB = Vocabulary(patterns.VOCAB)

VOCAB.term('USA', r"""
    U\.?S\.?A\.? | U\.?S\.?
    | United \s? States \s? of \s? America | United \s? States
    | U\.? \s? of \s? A\.?""")


def normalize_key(state: str) -> str:
    """Convert state abbreviations into a consistent key."""
    return regex.sub(r'[^a-z]+', '', state.lower())


def normalize_state(state: str) -> str:
    """Convert state abbreviations to the state name."""
    return NORMALIZE_US_STATE.get(normalize_key(state), state.title())


def build_state(state, postal, abbrev_blob):
    """Build patterns for a single state."""
    abbrevs = [fr'(?-i:{postal[0]}\.?{postal[1]}\.?)']
    abbrevs += [a.replace('.', r'\.?').replace(' ', r'\s?')
                for a in abbrev_blob.split(',') if a]

    abbrev_key = f'{postal}_abbrev'
    state_key = state.replace(' ', '_')
    state_value = state.replace(' ', r'\s?')

    STATE_NAMES.append(state_value)

    VOCAB.term(abbrev_key, abbrevs)
    VOCAB.term(state_key, state_value)
    VOCAB.grouper(postal, f'{abbrev_key} | {state_key}')

    for key in abbrevs:
        key = regex.sub(r'^\(\?-i:|\)$', '', key.lower())
        key = normalize_key(key)
        NORMALIZE_US_STATE[key] = state


def build_states():
    """Build state patterns."""
    df = pd.read_csv(STATE_CSV, na_filter=False, dtype=str)
    for _, row in df.iterrows():
        build_state(row['state'], row['postal'], row['abbrev'])
        STATES[row['state']] = row['postal']

    VOCAB.grouper('us_state', list(STATES.values()))


build_states()
STATE_NAMES = VOCAB.term('state_names', STATE_NAMES)
