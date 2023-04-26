from . import lat_long_action as act
from ... import const
from ..pattern_compiler import Compiler

SYM = r"""°"”“'`‘´’"""
PUNCT = f"{SYM},;._"
_180 = r"[-]?(1\d\d|\d\d?)([.,_;]\d+)?"
_90 = r"[-]?([1-9]\d|\d)([.,_;]\d+)?"
_60 = r"[-]?([1-6]\d|\d)([.,_;]\d+)?"

FLOAT_RE = r"^([\d,]+\.?\d*)\Z"
NUM_PLUS = r"^(±|\+|-)?[\d,]+\.?\d*\Z"
PLUS = r"^(±|\+|-)+\Z"
MINUS = r"^[-]\Z"


def decoder():
    return {
        ",": {"TEXT": {"REGEX": r"^[,;._:]\Z"}},
        "(": {"TEXT": {"IN": const.OPEN}},
        ")": {"TEXT": {"IN": const.CLOSE}},
        "key": {"ENT_TYPE": "lat_long_key"},
        "label": {"ENT_TYPE": "lat_long_label"},
        "deg": {"LOWER": {"REGEX": rf"""^([{SYM}]|degrees?|deg\.?)\Z"""}},
        "min": {"LOWER": {"REGEX": rf"""^([{SYM}]|minutes?|min\.?)\Z"""}},
        "sec": {"LOWER": {"REGEX": rf"""^([{SYM}]|seconds?|sec\.?)\Z"""}},
        "dir": {"LOWER": {"REGEX": r"""^[nesw]\.?\Z"""}},
        "180": {"TEXT": {"REGEX": rf"""^{_180}\Z"""}},
        "90": {"TEXT": {"REGEX": rf"""^{_90}\Z"""}},
        "60": {"TEXT": {"REGEX": rf"""^{_60}\Z"""}},
        "datum": {"ENT_TYPE": "datum"},
        "180E": {"LOWER": {"REGEX": rf"^{_180}[ew]\Z"}},
        "90N": {"LOWER": {"REGEX": rf"^{_90}[ns]\Z"}},
        "60'60": {"LOWER": {"REGEX": rf"^{_60}[{SYM}]{_60}[{SYM}]\Z"}},
        "60'60N": {"LOWER": {"REGEX": rf"^{_60}[{SYM}]{_60}[{SYM}][nesw]\Z"}},
        "m": {"ENT_TYPE": {"IN": ["metric_length", "imperial_length"]}},
        "99": {"TEXT": {"REGEX": FLOAT_RE}},
        "+99": {"TEXT": {"REGEX": NUM_PLUS}},
        "uncert": {"ENT_TYPE": "uncertain_label"},
        "lat_long": {"ENT_TYPE": "lat_long"},
        "[+]": {"TEXT": {"REGEX": PLUS}},
        "[-]": {"TEXT": {"REGEX": PLUS}},
    }


def lat_long_compilers():
    return Compiler(
        label="lat_long",
        on_match=act.LAT_LONG_MATCH,
        keep="lat_long",
        decoder=decoder(),
        patterns=[
            "label? [-]? 180 deg? 60 min? 60 sec? dir ,? [-]? 180 deg? 60 min? 60 sec? dir datum*",
            "label? [-]? 180 deg? 60 min?         dir ,? [-]? 180 deg? 60 min?         dir datum*",
            "label? [-]? 180E                         ,? [-]? 90N                          datum*",
            "label? [-]? 90N                          ,? [-]? 180E                         datum*",
            "label? [-]? 180 deg? 60'60  dir          ,? [-]? 180 deg? 60'60           dir datum*",
            "label? [-]? 180 deg? 60'60N              ,? [-]? 180 deg? 60'60N              datum*",
            "label? [-]? 180 deg? dir                 ,? [-]? 180 deg?                 dir datum*",
            "label? dir [-]? 180 deg? 60 min? 60 sec? ,? dir [-]? 180 deg? 60 min? 60 sec? datum*",
            "label? dir [-]? 180 deg? 60 min?         ,? dir [-]? 180 deg? 60 min?         datum*",
            "label? dir [-]? 180 deg? 60'60           ,? dir [-]? 180 deg? 60'60           datum*",
            "label? dir [-]? 180 deg?                 ,? dir [-]? 180 deg?                 datum*",
            "key ,? [-]? 90 key ,? [-]? 90",
            "key ,? [-]? 90 key ,? [-]? 90 ( datum+ )",
            "key ,? [-]? 90 key ,? [-]? 90   datum+",
        ],
    )


def lat_long_uncertain_compilers():
    return Compiler(
        label="lat_long_uncertain",
        id="lat_long",
        on_match=act.LAT_LONG_UNCERTAIN_MATCH,
        keep=["lat_long"],
        decoder=decoder(),
        patterns=[
            "lat_long+ ,? uncert? ,?     +99 m",
            "lat_long+ ,? uncert? ,? [+]? 99 m",
        ],
    )
