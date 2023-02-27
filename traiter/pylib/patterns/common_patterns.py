from traiter.pylib import const as t_const

AND = ["&", "and", "et"]
CONJ = AND + ["or"]
TO = ["to"]
UNDERLINE = ["_"]
MISSING = """
    no without missing lack lacking except excepting not rarely obsolete
    """.split()

COMMON_PATTERNS = {
    "any": {},
    "(": {"TEXT": {"IN": t_const.OPEN}},
    ")": {"TEXT": {"IN": t_const.CLOSE}},
    "-": {"TEXT": {"IN": t_const.DASH}, "OP": "+"},
    "[+]": {"TEXT": {"IN": t_const.PLUS}},
    "/": {"TEXT": {"IN": t_const.SLASH}},
    ",": {"TEXT": {"IN": t_const.COMMA}},
    ".": {"TEXT": {"IN": t_const.DOT}},
    "x": {"TEXT": {"IN": t_const.CROSS}},
    ":": {"TEXT": {"IN": t_const.COLON}},
    ";": {"TEXT": {"IN": t_const.SEMICOLON}},
    "[?]": {"TEXT": {"IN": t_const.Q_MARK}},
    "to": {"LOWER": {"IN": TO}},
    "-/or": {"LOWER": {"IN": t_const.DASH + TO + CONJ + UNDERLINE}, "OP": "+"},
    "-/to": {"LOWER": {"IN": t_const.DASH + TO + UNDERLINE}, "OP": "+"},
    "and": {"LOWER": {"IN": AND}},
    "and/or": {"LOWER": {"IN": CONJ}},
    "missing": {"LOWER": {"IN": MISSING}},
    "9": {"IS_DIGIT": True},
    "99-99": {"ENT_TYPE": "range"},
    "99.9-99.9": {"ENT_TYPE": "range"},
    "phrase": {"LOWER": {"REGEX": r"^([^.;:]+)$"}},
    "clause": {"LOWER": {"REGEX": r"^([^.;:,]+)$"}},
}
