import re
from pathlib import Path

from spacy import registry

from .. import terms
from .. import trait_util
from traiter.pipes.reject_match import RejectMatch
from traiter.pylib import const
from traiter.pylib import util

LAT_LONG_MATCH = "lat_long_match"
LAT_LONG_UNCERTAIN_MATCH = "lat_long_uncertain_match"

LAT_LONG_CSV = Path(__file__).parent / "lat_long_terms.csv"
UNIT_CSV = Path(terms.__file__).parent / "unit_length_terms.csv"

REPLACE = trait_util.term_data([UNIT_CSV, LAT_LONG_CSV], "replace")
FACTORS_CM = trait_util.term_data(UNIT_CSV, "factor_cm", float)
FACTORS_M = {k: v / 100.0 for k, v in FACTORS_CM.items()}

PUNCT = """{°"”“'`‘´’,;._"""
FLOAT_RE = r"^([\d,]+\.?\d*)$"


@registry.misc(LAT_LONG_MATCH)
def lat_long_match(ent):
    frags = []
    for token in ent:
        token._.flag = "lat_long"
        if token._.term == "lat_long_label":
            continue
        if token._.term == "datum":
            datum = REPLACE.get(token.lower_, token.text)
            ent._.data["datum"] = datum
        else:
            text = token.text.upper() if len(token.text) == 1 else token.text
            frags.append(text)

    lat_long = " ".join(frags)
    lat_long = re.sub(rf"\s([{PUNCT}])", r"\1", lat_long)
    lat_long = re.sub(rf"(-)\s", r"\1", lat_long)
    ent._.data["lat_long"] = lat_long

    ent[0]._.data = ent._.data  # Save for uncertainty in the lat/long
    ent[0]._.flag = "lat_long_data"


@registry.misc(LAT_LONG_UNCERTAIN_MATCH)
def lat_long_uncertain_match(ent):
    unit = ""
    value = 0.0
    for token in ent:
        # Get the data from the original parse
        if token._.flag == "lat_long_data":
            ent._.data = token._.data

        # Get the uncertainty units
        elif token._.term in ("metric_length", "imperial_length"):
            unit = REPLACE.get(token.lower_, token.lower_)

        # Already parse
        elif token._.flag:
            continue

        # Get the uncertainty value
        elif re.match(const.FLOAT_RE, token.text):
            value = util.to_positive_float(token.text)

    if not unit:
        raise RejectMatch()

    # Convert the values to meters
    ent._.data["units"] = "m"
    factor = FACTORS_M[unit]
    ent._.data["uncertainty"] = round(value * factor, 3)
