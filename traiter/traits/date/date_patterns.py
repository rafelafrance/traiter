from . import date_action as act
from traiter.traits.pattern_compiler import Compiler

SEP = ".,;/_'-"


def date_patterns():
    decoder = {
        "-": {"TEXT": {"REGEX": rf"^[{SEP}]\Z"}},
        "/": {"TEXT": {"REGEX": r"^/\Z"}},
        "99": {"TEXT": {"REGEX": r"^\d\d?\Z"}},
        "99-99": {"TEXT": {"REGEX": rf"^\d\d?[{SEP}]+\d\d\Z"}},
        "99-9999": {"TEXT": {"REGEX": rf"^\d\d?[{SEP}]+[12]\d\d\d\Z"}},
        "9999": {"TEXT": {"REGEX": r"^[12]\d{3}\Z"}},
        ":": {"TEXT": {"REGEX": r"^[:=]+\Z"}},
        "label": {"ENT_TYPE": "date_label"},
        "month": {"ENT_TYPE": "month"},
    }

    return [
        Compiler(
            label="date",
            decoder=decoder,
            on_match=act.DATE_MATCH,
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
            label="short_date",
            id="date",
            decoder=decoder,
            on_match=act.SHORT_DATE_MATCH,
            patterns=[
                "label? :? 9999  -* month",
                "label? :? month -* 9999",
                "label? :? 99-9999",
                "label? :? 99 / 9999",
            ],
        ),
    ]
