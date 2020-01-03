"""Patterns for US counties."""

from collections import defaultdict
import pandas as pd
from pylib.shared import util
from pylib.shared.parsers import us_states
from pylib.stacked_regex.rule_catalog import RuleCatalog

COUNTY_CSV = util.DATA_DIR / 'US_counties.csv'

CATALOG = RuleCatalog(us_states.CATALOG)


def build_counties():
    """Read the CSV file and build counties by state."""
    counties = defaultdict(list)
    df = pd.read_csv(COUNTY_CSV, na_filter=False, dtype=str)
    for _, row in df.iterrows():
        counties[row['State']].append(row['County'])

    us_county = []
    for abbrev in us_states.STATES.values():
        names = []
        for name in [n for n in counties[abbrev] if n not in us_states.STATES]:
            name = name.replace('.', r'\.?')
            name = name.replace("'", "'?")
            name = name.replace(' ', r'\s?')
            name = name.replace('-', r'[\s-]?')
            names.append(name)

        if not names:
            continue

        co_names = f'{abbrev}_co_names'
        CATALOG.term(co_names, names)

        state_co = f'{abbrev}_co'
        names = [n.replace(' ', '_')
                 for n in counties[abbrev] if n in us_states.STATES]
        CATALOG.grouper(state_co, [co_names] + names)

        us_county.append(state_co)
    CATALOG.grouper('us_county', us_county)


build_counties()
