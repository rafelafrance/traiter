from traiter.pylib.traits.pattern_compiler import Compiler


SEP = ".,;/_'-"
LABEL_ENDER = "[:=]"


def date_compilers():
    decoder = {
        "-": {"TEXT": {"REGEX": f"^[{SEP}]+$"}},
        "/": {"TEXT": {"REGEX": r"^/$"}},
        "99": {"TEXT": {"REGEX": r"^\d\d?$"}},
        "99-99": {"TEXT": {"REGEX": rf"^\d\d?[{SEP}]+\d\d$"}},
        "99-9999": {"TEXT": {"REGEX": rf"^\d\d?[{SEP}]+[12]\d\d\d$"}},
        "9999": {"TEXT": {"REGEX": r"^[12]\d{3}$"}},
        ":": {"TEXT": {"REGEX": f"^{LABEL_ENDER}+$"}},
        "label": {"ENT_TYPE": "date_label"},
        "month": {"ENT_TYPE": "month"},
    }

    return [
        Compiler(
            label="date",
            decoder=decoder,
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
            ],
        ),
        Compiler(
            label="date",
            decoder=decoder,
            id="short_date",
            patterns=[
                "label? :? 9999  -* month",
                "label? :? month -* 9999",
                "label? :? 99-9999",
                "label? :? 99 / 9999",
            ],
        ),
    ]
