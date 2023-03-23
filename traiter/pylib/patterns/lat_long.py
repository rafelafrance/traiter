import re

from spacy.util import registry

from . import terms_old
from .. import util
from traiter.pylib.pattern_compilers.matcher import Compiler


_SYM = r"""°"”“'`‘´’"""
_PUNCT = f"{_SYM},;._"
_180 = r"[-]?(1\d\d|\d\d?)([.,_;]\d+)?"
_90 = r"[-]?([1-9]\d|\d)([.,_;]\d+)?"
_60 = r"[-]?([1-6]\d|\d)([.,_;]\d+)?"

_FLOAT_RE = r"^([\d,]+\.?\d*)$"
_NUM_PLUS = r"^((±|\+|-)?[\d,]+\.?\d*)$"

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
}

# ###################################################################################
LAT_LONG = Compiler(
    "lat_long",
    on_match="digi_leap_lat_long_v1",
    decoder=_DECODER,
    patterns=[
        "label? 180 deg? 60 min? 60 sec? dir ,? 180 deg? 60 min? 60 sec? dir",
        "label? 180 deg? 60 min?         dir ,? 180 deg? 60 min?         dir",
        "label? 180E ,? 90N  datum?",
        "label? 90N  ,? 180E datum?",
        "label? 180 deg? 60'60  dir ,? 180 deg? 60'60  dir",
        "label? 180 deg? 60'60N     ,? 180 deg? 60'60N",
        "label? 180 deg? dir        ,? 180 deg? dir",
        "label? dir 180 deg? 60 min? 60 sec? ,? dir 180 deg? 60 min? 60 sec?",
        "label? dir 180 deg? 60 min?         ,? dir 180 deg? 60 min?",
        "label? dir 180 deg? 60'60  ,? dir 180 deg? 60'60",
        "label? dir 180 deg?        ,? dir 180 deg?",
    ],
)


@registry.misc(LAT_LONG.on_match)
def on_lat_long_match(ent):
    parts = []
    for token in ent:
        if token.ent_type_ == "lat_long_label":
            continue
        if token.ent_type_ == "datum":
            ent._.data["datum"] = terms.LAT_LONG_TERMS.replace.get(
                token.lower_, token.text
            )
        else:
            text = token.text.upper() if len(token.text) == 1 else token.text
            parts.append(text)

    lat_long = " ".join(parts)
    lat_long = re.sub(rf"\s([{_PUNCT}])", r"\1", lat_long)
    ent._.data["lat_long"] = lat_long
    ent[0]._.data = ent._.data


# ########################################################c###########################
LAT_LONG_UNCERTAIN = Compiler(
    "lat_long_uncert",
    on_match="digi_leap_lat_long_uncert_v1",
    decoder=_DECODER,
    patterns=[
        "lat_long+ ,?        ,? +99 m",
        "lat_long+ ,? uncert ,?  99 m",
    ],
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
            units = terms.LAT_LONG_TERMS.replace.get(token.lower_, token.lower_)

    factor = terms.FACTORS_M[units]
    ent._.data["uncertainty"] = round(value * factor, 3)
    ent._.new_label = "lat_long"
