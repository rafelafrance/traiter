import re
from pathlib import Path

from spacy.language import Language
from spacy.util import registry

from traiter.pylib import const, term_util, util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

LABEL_ENDER = r"[:=;,.]"
FLOAT_RE = r"^(\d[\d,.]+)\Z"
UNITS = ["metric_length", "imperial_length"]

ELEVATION_CSV = Path(__file__).parent / "terms" / "elevation_terms.csv"
UNIT_CSV = Path(__file__).parent / "terms" / "unit_length_terms.csv"
ABOUT_CSV = Path(__file__).parent / "terms" / "about_terms.csv"
ALL_CSVS = [ELEVATION_CSV, UNIT_CSV, ABOUT_CSV]

REPLACE = term_util.term_data([UNIT_CSV, ELEVATION_CSV], "replace")
FACTORS_CM = term_util.term_data(UNIT_CSV, "factor_cm", float)
FACTORS_M = {k: v / 100.0 for k, v in FACTORS_CM.items()}


def build(nlp: Language):
    add.term_pipe(nlp, name="elevation_terms", path=ALL_CSVS)
    add.trait_pipe(nlp, name="elevation_patterns", compiler=elevation_compilers())
    add.cleanup_pipe(nlp, name="elevation_cleanup")


def elevation_compilers():
    decoder = {
        "(": {"TEXT": {"IN": const.OPEN}},
        ")": {"TEXT": {"IN": const.CLOSE}},
        "-/to": {"LOWER": {"IN": [*const.DASH, "to", "_"]}, "OP": "+"},
        "/": {"TEXT": {"IN": const.SLASH}},
        "99": {"TEXT": {"REGEX": FLOAT_RE}},
        ":": {"TEXT": {"REGEX": rf"^{LABEL_ENDER}+\Z"}},
        ",": {"TEXT": {"REGEX": rf"^{LABEL_ENDER}+\Z"}},
        "about": {"ENT_TYPE": "about"},
        "label": {"ENT_TYPE": "elev_label"},
        "m": {"ENT_TYPE": {"IN": UNITS}},
    }

    return [
        Compiler(
            label="elevation",
            decoder=decoder,
            on_match="elevation_match",
            keep="elevation",
            patterns=[
                "label+ :? about? ,? 99 m",
                "label+ :? about? ,? 99 m ( 99 m )",
                "label+ :? about? ,? 99 m / 99 m",
                "          about? ,? 99 m ( 99 m )",
                "          about? ,? 99 m / 99 m",
            ],
        ),
        Compiler(
            label="elevation_range",
            id="elevation",
            on_match="elevation_match",
            decoder=decoder,
            keep="elevation",
            patterns=[
                "label+ :? about? ,? 99 -/to 99 m",
            ],
        ),
    ]


@registry.misc("elevation_match")
def elevation_match(ent):
    values = []
    units_ = ""
    expected_len = 1
    about = False

    for token in ent:
        # Find numbers
        if re.match(const.FLOAT_RE, token.text) and len(values) < expected_len:
            values.append(util.to_positive_float(token.text))

        # Find units
        elif token._.term in UNITS and not units_:
            units_ = REPLACE.get(token.lower_, token.lower_)

        elif token._.term == "about":
            about = True

        # If there's a dash it's a range
        elif token.lower_ in [*const.DASH, "to", "_"]:
            expected_len = 2

    factor = FACTORS_M[units_]

    ent._.data = {
        "elevation": round(values[0] * factor, 3),
        "units": "m",
    }
    if about:
        ent._.data["about"] = True

    # Handle an elevation range
    if expected_len == 2:
        ent._.data["elevation_high"] = round(values[1] * factor, 3)
