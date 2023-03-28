from ...pattern_compilers.matcher import Compiler

_SYM = r"""°"”“'`‘´’"""
_PUNCT = f"{_SYM},;._"
_180 = r"[-]?(1\d\d|\d\d?)([.,_;]\d+)?"
_90 = r"[-]?([1-9]\d|\d)([.,_;]\d+)?"
_60 = r"[-]?([1-6]\d|\d)([.,_;]\d+)?"

_FLOAT_RE = r"^([\d,]+\.?\d*)$"
_NUM_PLUS = r"^((±|\+|-)?[\d,]+\.?\d*)$"
_PLUS = r"^(±|\+|-)+$"
_MINUS = r"^[-]$"

_UNITS = ["metric_dist", "imperial_dist"]

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

LAT_LONG = Compiler(
    label="lat_long",
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
)

LAT_LONG_UNCERTAIN = Compiler(
    label="lat_long",
    decoder=_DECODER,
    patterns=[
        "lat_long+ ,? uncert? ,?     +99 m",
        "lat_long+ ,? uncert? ,? [+]? 99 m",
    ],
)
