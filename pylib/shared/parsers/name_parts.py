"""Patterns for names."""

import pandas as pd
from pylib.shared import util
from pylib.shared import patterns
from pylib.stacked_regex.rule_catalog import RuleCatalog

NAME_CSV = util.DATA_DIR / 'name_parts.csv'

CATALOG = RuleCatalog(patterns.CATALOG)


def build_name_parts():
    """Build name patterns."""
    df = pd.read_csv(NAME_CSV, na_filter=False, dtype=str)
    CATALOG.term('name_part', df['name'].tolist(), capture=False)


build_name_parts()
