from ... import const
from traiter.pylib.matcher_compiler import Compiler

_LABEL_ENDER = r"[:=;,.]"
_UNITS = ["metric_length", "imperial_length"]
_FLOAT_RE = r"^(\d[\d,.]+)$"

_DECODER = {
    "(": {"TEXT": {"IN": const.OPEN}},
    ")": {"TEXT": {"IN": const.CLOSE}},
    "/": {"TEXT": {"IN": const.SLASH}},
    "99": {"TEXT": {"REGEX": _FLOAT_RE}},
    ":": {"TEXT": {"REGEX": f"^{_LABEL_ENDER}+$"}},
    "label": {"ENT_TYPE": "elev_label"},
    "m": {"ENT_TYPE": {"IN": _UNITS}},
}

ELEVATION = Compiler(
    label="elevation",
    decoder=_DECODER,
    patterns=[
        "label :? 99 m",
        "label :? 99 m ( 99 m )",
        "label :? 99 m / 99 m",
    ],
)

ELEVATION_RANGE = Compiler(
    label="elevation_range",
    decoder=_DECODER,
    patterns=[
        "label :? 99 - 99 m",
    ],
)
