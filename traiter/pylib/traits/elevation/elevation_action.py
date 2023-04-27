import re
from pathlib import Path

from spacy.util import registry

from traiter.pylib import const
from traiter.pylib import util
from traiter.pylib.traits import terms
from traiter.pylib.traits import trait_util

ELEVATION_MATCH = "elevation_match"

UNITS = ("metric_length", "imperial_length")

ELEVATION_CSV = Path(__file__).parent / "elevation_terms.csv"
UNIT_CSV = Path(terms.__file__).parent / "unit_length_terms.csv"
ABOUT_CSV = Path(terms.__file__).parent / "about.csv"
ALL_CSVS = [ELEVATION_CSV, UNIT_CSV, ABOUT_CSV]


REPLACE = trait_util.term_data([UNIT_CSV, ELEVATION_CSV], "replace")
FACTORS_CM = trait_util.term_data(UNIT_CSV, "factor_cm", float)
FACTORS_M = {k: v / 100.0 for k, v in FACTORS_CM.items()}


@registry.misc(ELEVATION_MATCH)
def elevation_match(ent):
    values = []
    units_ = ""
    expected_len = 1
    about = False

    for token in ent:
        # Find numbers
        if re.match(const.FLOAT_RE, token.text) and len(values) < expected_len:
            values.append(util.to_positive_float(token.text))

        # Find units
        elif token._.term in UNITS and not units_:
            units_ = REPLACE.get(token.lower_, token.lower_)

        elif token._.term == "about":
            about = True

        # If there's a dash it's a range
        elif token.lower_ in const.DASH + ["to", "_"]:
            expected_len = 2

    factor = FACTORS_M[units_]

    ent._.data = {
        "elevation": round(values[0] * factor, 3),
        "units": "m",
    }
    if about:
        ent._.data["about"] = True

    # Handle an elevation range
    if expected_len == 2:
        ent._.data["elevation_high"] = round(values[1] * factor, 3)
