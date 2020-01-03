"""
Read ITIS taxonomues and add them to the catalog.

SELECT DISTINCT complete_name
 FROM taxonomic_units
WHERE kingdom_id = 3     -- 3 = Plants
  AND rank_id = 180      -- 180 = genus, 140 = family
ORDER BY complete_name;
"""

import pandas as pd
from pylib.shared import util
from pylib.stacked_regex.rule_catalog import RuleCatalog

PLANT_FAMILIES = util.DATA_DIR / 'itis_plant_families.csv'
PLANT_GENERA = util.DATA_DIR / 'itis_plant_genera.csv'


def build_families(catalog: RuleCatalog) -> None:
    """Build patterns for recognizing taxa."""
    df = pd.read_csv(PLANT_FAMILIES, na_filter=False, dtype=str)
    catalog.term('plant_family', df['complete_name'].tolist())


def build_genera(catalog: RuleCatalog) -> None:
    """Build patterns for recognizing taxa."""
    df = pd.read_csv(PLANT_GENERA, na_filter=False, dtype=str)
    catalog.term('plant_genus', df['complete_name'].tolist())
