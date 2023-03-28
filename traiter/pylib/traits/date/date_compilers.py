from traiter.pylib.matcher_compiler import Compiler

_SEP = "[.,;/_'-]"
_LABEL_ENDER = "[:=]"
_LABELS = """ date """.split()

_DECODER = {
    "-": {"TEXT": {"REGEX": f"^{_SEP}+$"}},
    "/": {"TEXT": {"REGEX": r"^/$"}},
    "99": {"TEXT": {"REGEX": r"^\d\d?$"}},
    "99-99": {"TEXT": {"REGEX": rf"^\d\d?{_SEP}+\d\d$"}},
    "99-9999": {"TEXT": {"REGEX": rf"^\d\d?{_SEP}+[12]\d\d\d$"}},
    "9999": {"TEXT": {"REGEX": r"^[12]\d{3}$"}},
    ":": {"TEXT": {"REGEX": f"^{_LABEL_ENDER}+$"}},
    "label": {"LOWER": {"IN": _LABELS}},
    "month": {"ENT_TYPE": "month"},
    # "99-99-9999": {"TEXT": {"REGEX": rf"^\d\d?{_SEP}+\d\d?{_SEP}+[12]\d\d\d$"}},
    # "9999-99-99": {"TEXT": {"REGEX": rf"^[12]\d\d\d?{_SEP}+\d\d?{_SEP}+\d\d?$"}},
    # "99-99-99": {"TEXT": {"REGEX": rf"^\d\d?{_SEP}+\d\d?{_SEP}+\d\d$"}},
    # "month-99-9999": {"LOWER": {"REGEX": rf"^[a-z]+{_SEP}+\d\d?{_SEP}+[12]\d\d\d$"}},
}

DATE = Compiler(
    label="date",
    decoder=_DECODER,
    patterns=[
        "label? :? 99    -* month -* 99",
        "label? :? 99    -* month -* 9999",
        "label? :? 9999  -* month -* 99",
        "label? :? 99    -  99    -  99",
        "label? :? 99    -  99    -  9999",
        "label? :? month -* 99    -* 9999",
        "label? :? 9999  -  99    -  99",
        "label? :? month -* 99-9999",
        "label? :? month -* 99-99",
        # "label? :? month -* 99 -* 9999",
        # "label? :? 99-99-9999",
        # "label? :? 99-99-99",
    ],
)

MISSING_DAYS = Compiler(
    label="short_date",
    decoder=_DECODER,
    patterns=[
        "label? :? 9999  -* month",
        "label? :? month -* 9999",
        "label? :? 99-9999",
        "label? :? 99 / 9999",
    ],
)
