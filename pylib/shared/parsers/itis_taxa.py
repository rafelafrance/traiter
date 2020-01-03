"""Read ITIS taxonomues and add them to the catalog."""

import pandas as pd
from pylib.shared import util
from pylib.shared import db
from pylib.stacked_regex.rule import Rule, term
from pylib.stacked_regex.rule_catalog import RuleCatalog

ITIS_DB = util.DATA_DIR / 'shared' / 'itisSqlite121919' / 'ITIS.sqlite'

KINGDOMS = {}
RANKS = {}


def build_kingdoms():
    """Get the kingdom codes from the ITIS database."""
    sql = """SELECT kingdom_id, kingdom_name FROM kingdoms;"""

    with db.connect(ITIS_DB) as cxn:
        df = pd.read_sql(sql, cxn)

    for _, row in df.iterrows():
        KINGDOMS[row['kingdom_name'].lower()] = row['kingdom_id']

    # Get vernacular names for kingdoms
    sql = """
        SELECT vernacular_name, kingdom_id
          FROM taxonomic_units
          JOIN vernaculars USING (tsn)
         WHERE rank_id = 10;"""

    with db.connect(ITIS_DB) as cxn:
        df = pd.read_sql(sql, cxn)

    for _, row in df.iterrows():
        name = row['vernacular_name'].lower()
        KINGDOMS[name] = row['kingdom_id']
        if name[-1] == 's' and name[-2] not in 'aeiou':
            KINGDOMS[name[:-1]] = row['kingdom_id']


def build_ranks():
    """Get taxa ranks from the ITIS database."""
    sql = """SELECT kingdom_id, rank_id, rank_name FROM taxon_unit_types;"""

    with db.connect(ITIS_DB) as cxn:
        df = pd.read_sql(sql, cxn)

    for _, row in df.iterrows():
        rank = row['rank_name'].lower()
        RANKS[(row['kingdom_id'], rank)] = row['rank_id']


def build_rule(catalog: RuleCatalog, kingdom: str, rank: str) -> None:
    """Build patterns for recognizing taxa."""
    kingdom = kingdom.lower()
    rank = rank.lower()

    if not KINGDOMS:
        build_kingdoms()
        build_ranks()

    kingdom_id = KINGDOMS[kingdom]
    rank_id = RANKS[(kingdom_id, rank)]

    sql = """
        SELECT DISTINCT complete_name
          FROM taxonomic_units
         WHERE kingdom_id = ?
           AND rank_id = ?
      ORDER BY complete_name;"""

    with db.connect(ITIS_DB) as cxn:
        df = pd.read_sql(sql, cxn, params=(kingdom_id, rank_id))

    catalog.term(f'{kingdom}_{rank}', df['complete_name'].tolist())
