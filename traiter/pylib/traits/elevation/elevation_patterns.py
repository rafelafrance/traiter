from . import elevation_action as act
from traiter.pylib import const
from traiter.pylib.traits.pattern_compiler import Compiler

LABEL_ENDER = r"[:=;,.]"
UNITS = ["metric_length", "imperial_length"]
FLOAT_RE = r"^(\d[\d,.]+)\Z"
TO = ["to"]
UNDERLINE = ["_"]


def elevation_compilers():
    decoder = {
        "(": {"TEXT": {"IN": const.OPEN}},
        ")": {"TEXT": {"IN": const.CLOSE}},
        "-/to": {"LOWER": {"IN": const.DASH + ["to", "_"]}, "OP": "+"},
        "/": {"TEXT": {"IN": const.SLASH}},
        "99": {"TEXT": {"REGEX": FLOAT_RE}},
        ":": {"TEXT": {"REGEX": rf"^{LABEL_ENDER}+\Z"}},
        "label": {"ENT_TYPE": "elev_label"},
        "m": {"ENT_TYPE": {"IN": UNITS}},
    }

    return [
        Compiler(
            label="elevation",
            decoder=decoder,
            on_match=act.ELEVATION_MATCH,
            patterns=[
                "label+ :? 99 m",
                "label+ :? 99 m ( 99 m )",
                "label+ :? 99 m / 99 m",
            ],
        ),
        Compiler(
            label="elevation_range",
            id="elevation",
            on_match=act.ELEVATION_MATCH,
            decoder=decoder,
            patterns=[
                "label+ :? 99 -/to 99 m",
            ],
        ),
    ]
