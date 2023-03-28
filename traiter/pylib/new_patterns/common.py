from pathlib import Path

from .. import const
from .. import new_patterns

PATTERN_DIR = Path(new_patterns.__file__).parent

AND = ["&", "and", "et"]
CONJ = AND + ["or"]
TO = ["to"]
UNDERLINE = ["_"]
MISSING = """
    no without missing lack lacking except excepting not rarely obsolete
    """.split()

PATTERNS = {
    "any": {},
    "(": {"TEXT": {"IN": const.OPEN}},
    ")": {"TEXT": {"IN": const.CLOSE}},
    "-": {"TEXT": {"IN": const.DASH}, "OP": "+"},
    "[+]": {"TEXT": {"IN": const.PLUS}},
    "/": {"TEXT": {"IN": const.SLASH}},
    ",": {"TEXT": {"IN": const.COMMA}},
    ".": {"TEXT": {"IN": const.DOT}},
    "x": {"TEXT": {"IN": const.CROSS}},
    ":": {"TEXT": {"IN": const.COLON}},
    ";": {"TEXT": {"IN": const.SEMICOLON}},
    "[?]": {"TEXT": {"IN": const.Q_MARK}},
    "to": {"LOWER": {"IN": TO}},
    "-/or": {"LOWER": {"IN": const.DASH + TO + CONJ + UNDERLINE}, "OP": "+"},
    "-/to": {"LOWER": {"IN": const.DASH + TO + UNDERLINE}, "OP": "+"},
    "and": {"LOWER": {"IN": AND}},
    "and/or": {"LOWER": {"IN": CONJ}},
    "missing": {"LOWER": {"IN": MISSING}},
    "9": {"IS_DIGIT": True},
    "99-99": {"ENT_TYPE": "range"},
    "99.9-99.9": {"ENT_TYPE": "range"},
    "phrase": {"LOWER": {"REGEX": r"^([^.;:]+)$"}},
    "clause": {"LOWER": {"REGEX": r"^([^.;:,]+)$"}},
}
