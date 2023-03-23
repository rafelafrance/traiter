import re

from spacy.util import registry

from . import common
from . import terms_old
from .. import util
from ..pattern_compilers.matcher import Compiler


_LABEL_ENDER = r"[:=;,.]"
_UNITS = ["metric_length", "imperial_length"]

_FLOAT_RE = r"^(\d[\d,.]+)$"

_DECODER = common.PATTERNS | {
    "label": {"ENT_TYPE": "elev_label"},
    ":": {"TEXT": {"REGEX": f"^{_LABEL_ENDER}+$"}},
    "99": {"TEXT": {"REGEX": _FLOAT_RE}},
    "m": {"ENT_TYPE": {"IN": _UNITS}},
}

# ####################################################################################
ELEVATION = Compiler(
    "elevation",
    on_match="traiter_elevation_v1",
    decoder=_DECODER,
    patterns=[
        "label :? 99 m",
        "label :? 99 m ( 99 m )",
    ],
)


@registry.misc(ELEVATION.on_match)
def on_elevation_match(ent):
    values = []
    units = []

    for token in ent:
        if re.match(_FLOAT_RE, token.text):
            values.append(util.to_positive_float(token.text))
        elif token.ent_type_ in _UNITS:
            units.append(terms.ELEV_TERMS.replace.get(token.lower_, token.lower_))

    factor = terms.FACTORS_M[units[0]]
    ent._.data["elevation"] = round(values[0] * factor, 3)


# ####################################################################################
ELEVATION_RANGE = Compiler(
    "elevation_range",
    on_match="traiter_elevation_range_v1",
    decoder=_DECODER,
    patterns=[
        "label :? 99 - 99 m",
    ],
)


@registry.misc(ELEVATION_RANGE.on_match)
def on_elevation_range_match(ent):
    values = []
    units = ""

    for token in ent:
        if re.match(_FLOAT_RE, token.text):
            values.append(util.to_positive_float(token.text))
        elif token.ent_type_ in _UNITS:
            units = terms.ELEV_TERMS.replace.get(token.lower_, token.lower_)

    factor = terms.FACTORS_M[units]
    ent._.data["elevation"] = round(values[0] * factor, 3)
    ent._.data["elevation_high"] = round(values[1] * factor, 3)
    ent._.new_label = "elevation"
