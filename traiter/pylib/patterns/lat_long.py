import re

from spacy.util import registry

from . import common
from ..term_list import TermList
from traiter.pylib.pattern_compilers.matcher import Compiler

_SYMBOLS = r"""°"”“'`‘´’"""
_PUNCT = f"""{_SYMBOLS},;._"""

TERMS = TermList.shared("lat_long")

LAT_LONG = Compiler(
    "lat_long",
    on_match="digi_leap_lat_long_v1",
    decoder=common.PATTERNS
    | {
        "label": {"ENT_TYPE": "lat_long_label"},
        "deg": {"LOWER": {"REGEX": rf"""^([{_SYMBOLS}]|degrees?|deg\.?)$"""}},
        "min": {"LOWER": {"REGEX": rf"""^([{_SYMBOLS}]|minutes?|min\.?)$"""}},
        "sec": {"LOWER": {"REGEX": rf"""^([{_SYMBOLS}]|seconds?|sec\.?)$"""}},
        "dir": {"LOWER": {"REGEX": r"""^[nesw]\.?$"""}},
        "180": {"TEXT": {"REGEX": r"""^[-]?(1?[0-8]\d|\d{1,2})([.,_;]\d+)?$"""}},
        "90": {"TEXT": {"REGEX": r"""^[-]?([0-8]?\d?)([.,_;]\d+)?$"""}},
        "60": {"TEXT": {"REGEX": r"""^[-]?([1-5]?\d?)([.,_;]\d+)?$"""}},
        "ew": {"LOWER": {"REGEX": r"""^[ew]\.?$"""}},
        "ns": {"LOWER": {"REGEX": r"""^[ns]\.?$"""}},
        "datum": {"ENT_TYPE": "datum"},
    },
    patterns=[
        "label? 180 deg? 60 min? 60 sec? dir ,? 180 deg? 60 min? 60 sec? dir",
        "label? 180 deg? 60 min?         dir ,? 180 deg? 60 min?         dir",
        "label? 180 ew ,? 90 ns datum?",
        "label? 90 ns ,? 180 ew datum?",
    ],
)


@registry.misc(LAT_LONG.on_match)
def on_lat_long_match(ent):
    parts = []
    for token in ent:
        if token.ent_type_ == "lat_long_label":
            continue
        if token.ent_type_ == "datum":
            ent._.data["datum"] = TERMS.replace.get(token.lower_, token.text)
        else:
            parts.append(token.text.upper())

    lat_long = " ".join(parts)
    lat_long = re.sub(rf"\s([{_PUNCT}])", r"\1", lat_long)
    ent._.data["lat_long"] = lat_long
