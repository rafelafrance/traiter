import re

from spacy.util import registry

from .. import util
from ..matcher_patterns import MatcherPatterns
from ..vocabulary.terms import TERMS

_SYM = r"""°"”“'`‘´’"""
_PUNCT = f"{_SYM},;._"
_180 = r"[-]?(1\d\d|\d\d?)([.,_;]\d+)?"
_90 = r"[-]?([1-9]\d|\d)([.,_;]\d+)?"
_60 = r"[-]?([1-6]\d|\d)([.,_;]\d+)?"

_FLOAT_RE = r"^([\d,]+\.?\d*)$"
_NUM_PLUS = r"^((±|\+|-)?[\d,]+\.?\d*)$"
_PLUS = r"^(±|\+|-)+$"
_MINUS = r"^[-]$"

_UNITS = ["metric_length", "imperial_length"]

_DECODER = {
    ",": {"TEXT": {"REGEX": r"^[,;._:]$"}},
    "label": {"ENT_TYPE": "lat_long_label"},
    "deg": {"LOWER": {"REGEX": rf"""^([{_SYM}]|degrees?|deg\.?)$"""}},
    "min": {"LOWER": {"REGEX": rf"""^([{_SYM}]|minutes?|min\.?)$"""}},
    "sec": {"LOWER": {"REGEX": rf"""^([{_SYM}]|seconds?|sec\.?)$"""}},
    "dir": {"LOWER": {"REGEX": r"""^[nesw]\.?$"""}},
    "180": {"TEXT": {"REGEX": rf"""^{_180}$"""}},
    "90": {"TEXT": {"REGEX": rf"""^{_90}$"""}},
    "60": {"TEXT": {"REGEX": rf"""^{_60}$"""}},
    "datum": {"ENT_TYPE": "datum"},
    "180E": {"LOWER": {"REGEX": rf"^{_180}[ew]$"}},
    "90N": {"LOWER": {"REGEX": rf"^{_90}[ns]$"}},
    "60'60": {"LOWER": {"REGEX": rf"^{_60}[{_SYM}]{_60}[{_SYM}]$"}},
    "60'60N": {"LOWER": {"REGEX": rf"^{_60}[{_SYM}]{_60}[{_SYM}][nesw]$"}},
    "m": {"ENT_TYPE": {"IN": _UNITS}},
    "99": {"TEXT": {"REGEX": _FLOAT_RE}},
    "+99": {"TEXT": {"REGEX": _NUM_PLUS}},
    "uncert": {"ENT_TYPE": "uncertain_label"},
    "lat_long": {"ENT_TYPE": "lat_long"},
    "[+]": {"TEXT": {"REGEX": _PLUS}},
    "[-]": {"TEXT": {"REGEX": _PLUS}},
}

_FACTORS_CM = TERMS.pattern_dict("factor_cm", float)  # Convert value to cm
_FACTORS_M = {k: v / 100.0 for k, v in _FACTORS_CM.items()}  # Convert value to meters

# ###################################################################################
LAT_LONGS = MatcherPatterns(
    name="lat_long",
    on_match="digi_leap_lat_long_v1",
    decoder=_DECODER,
    patterns=[
        "label? [-]? 180 deg? 60 min? 60 sec? dir ,? [-]? 180 deg? 60 min? 60 sec? dir datum?",
        "label? [-]? 180 deg? 60 min?         dir ,? [-]? 180 deg? 60 min?         dir datum?",
        "label? [-]? 180E                         ,? [-]? 90N                          datum?",
        "label? [-]? 90N                          ,? [-]? 180E                         datum?",
        "label? [-]? 180 deg? 60'60  dir          ,? [-]? 180 deg? 60'60           dir datum?",
        "label? [-]? 180 deg? 60'60N              ,? [-]? 180 deg? 60'60N              datum?",
        "label? [-]? 180 deg? dir                 ,? [-]? 180 deg?                 dir datum?",
        "label? dir [-]? 180 deg? 60 min? 60 sec? ,? dir [-]? 180 deg? 60 min? 60 sec? datum?",
        "label? dir [-]? 180 deg? 60 min?         ,? dir [-]? 180 deg? 60 min?         datum?",
        "label? dir [-]? 180 deg? 60'60           ,? dir [-]? 180 deg? 60'60           datum?",
        "label? dir [-]? 180 deg?                 ,? dir [-]? 180 deg?                 datum?",
    ],
    output=["lat_long"],
)


@registry.misc(LAT_LONGS.on_match)
def on_lat_long_match(ent):
    parts = []
    for token in ent:
        if token.ent_type_ == "lat_long_label":
            continue
        if token.ent_type_ == "datum":
            ent._.data["datum"] = TERMS.replace.get(token.lower_, token.text)
        else:
            text = token.text.upper() if len(token.text) == 1 else token.text
            parts.append(text)

    lat_long = " ".join(parts)
    lat_long = re.sub(rf"\s([{_PUNCT}])", r"\1", lat_long)
    lat_long = re.sub(rf"(-)\s", r"\1", lat_long)
    ent._.data["lat_long"] = lat_long
    ent[0]._.data = ent._.data


# ####################################################################################
LAT_LONG_UNCERTAIN = MatcherPatterns(
    name="lat_long_uncertain",
    on_match="digi_leap_lat_long_uncertain_v1",
    decoder=_DECODER,
    patterns=[
        "lat_long+ ,? uncert? ,?     +99 m",
        "lat_long+ ,? uncert? ,? [+]? 99 m",
    ],
    output=["lat_long"],
)


@registry.misc(LAT_LONG_UNCERTAIN.on_match)
def on_lat_long_match(ent):
    value = 0.0
    units = ""
    for token in ent:
        label = token.ent_type_
        if label == "lat_long":
            ent._.data = token._.data
        elif re.match(_NUM_PLUS, token.text):
            value = util.to_positive_float(token.text)
        elif label in _UNITS:
            units = TERMS.replace.get(token.lower_, token.lower_)

    factor = _FACTORS_M[units]
    ent._.data["uncertainty"] = round(value * factor, 3)
    ent._.new_label = "lat_long"
