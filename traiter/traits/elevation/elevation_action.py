import re
from pathlib import Path

from spacy import registry

from .. import terms
from .. import trait_util
from traiter.pylib import const
from traiter.pylib import util

ELEVATION_MATCH = "elevation_match"

UNITS = ("metric_length", "imperial_length")

ELEVATION_CSV = Path(__file__).parent / "elevation_terms.csv"
UNIT_CSV = Path(terms.__file__).parent / "unit_length_terms.csv"

REPLACE = trait_util.term_data([UNIT_CSV, ELEVATION_CSV], "replace")
FACTORS_CM = trait_util.term_data(UNIT_CSV, "factor_cm", float)
FACTORS_M = {k: v / 100.0 for k, v in FACTORS_CM.items()}


@registry.misc(ELEVATION_MATCH)
def elevation_match(ent):
    values = []
    units_ = ""
    expected_len = 1

    for token in ent:
        # Find numbers
        if re.match(const.FLOAT_RE, token.text) and len(values) < expected_len:
            values.append(util.to_positive_float(token.text))

        # Find units
        elif token._.term in UNITS and not units_:
            units_ = REPLACE.get(token.lower_, token.lower_)

        # If there's a dash it's a range
        elif token.lower_ in const.DASH + ["to", "_"]:
            expected_len = 2

    ent._.data["units"] = "m"
    factor = FACTORS_M[units_]
    ent._.data["elevation"] = round(values[0] * factor, 3)

    # Handle a elevation range
    if expected_len == 2:
        ent._.data["elevation_high"] = round(values[1] * factor, 3)
