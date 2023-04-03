from ... import const
from traiter.pylib.traits.pattern_compiler import Compiler

LABEL_ENDER = r"[:=;,.]"
UNITS = ["metric_length", "imperial_length"]
FLOAT_RE = r"^(\d[\d,.]+)$"

DECODER = {
    "(": {"TEXT": {"IN": const.OPEN}},
    ")": {"TEXT": {"IN": const.CLOSE}},
    "-": {"LOWER": {"IN": const.DASH}, "OP": "+"},
    "/": {"TEXT": {"IN": const.SLASH}},
    "99": {"TEXT": {"REGEX": FLOAT_RE}},
    ":": {"TEXT": {"REGEX": f"^{LABEL_ENDER}+$"}},
    "label": {"ENT_TYPE": "elev_label"},
    "m": {"ENT_TYPE": {"IN": UNITS}},
}

ELEVATION_COMPILERS = [
    Compiler(
        label="elevation",
        decoder=DECODER,
        patterns=[
            "label :? 99 m",
            "label :? 99 m ( 99 m )",
            "label :? 99 m / 99 m",
        ],
    ),
    Compiler(
        label="elevation",
        id="elevation_range",
        decoder=DECODER,
        patterns=[
            "label :? 99 - 99 m",
        ],
    ),
]
