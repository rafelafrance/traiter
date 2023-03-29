from ... import const
from ...matcher_compiler import Compiler

LABEL_ENDER = r"[:=;,.]"
UNITS = ["metric_length", "imperial_length"]
FLOAT_RE = r"^(\d[\d,.]+)$"

_DECODER = {
    "(": {"TEXT": {"IN": const.OPEN}},
    ")": {"TEXT": {"IN": const.CLOSE}},
    "-": {"LOWER": {"IN": const.DASH}, "OP": "+"},
    "/": {"TEXT": {"IN": const.SLASH}},
    "99": {"TEXT": {"REGEX": FLOAT_RE}},
    ":": {"TEXT": {"REGEX": f"^{LABEL_ENDER}+$"}},
    "label": {"ENT_TYPE": "elev_label"},
    "m": {"ENT_TYPE": {"IN": UNITS}},
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
    label="elevation",
    id="elevation_range",
    decoder=_DECODER,
    patterns=[
        "label :? 99 - 99 m",
    ],
)

COMPILERS = [ELEVATION, ELEVATION_RANGE]
