import re

from spacy.util import registry

from . import common
from ..term_list import TermList
from traiter.pylib.pattern_compilers.matcher import Compiler

LAT_LONG_TERMS = TermList.shared("lat_long")

_SYM = r"""°"”“'`‘´’"""
_PUNCT = f"{_SYM},;._"
_180 = r"[-]?(1\d\d|\d\d?)([.,_;]\d+)?"
_90 = r"[-]?([1-9]\d|\d)([.,_;]\d+)?"
_60 = r"[-]?([1-6]\d|\d)([.,_;]\d+)?"

LAT_LONG = Compiler(
    "lat_long",
    on_match="digi_leap_lat_long_v1",
    decoder={
        ",": {"TEXT": {"REGEX": r"^[,;._]$"}},
        "label": {"ENT_TYPE": "lat_long_label"},
        "deg": {"LOWER": {"REGEX": rf"""^([{_SYM}]|degrees?|deg\.?)$"""}},
        "min": {"LOWER": {"REGEX": rf"""^([{_SYM}]|minutes?|min\.?)$"""}},
        "sec": {"LOWER": {"REGEX": rf"""^([{_SYM}]|seconds?|sec\.?)$"""}},
        "dir": {"LOWER": {"REGEX": r"""^[nesw]\.?$"""}},
        "180": {"TEXT": {"REGEX": rf"""^{_180}$"""}},
        "90": {"TEXT": {"REGEX": rf"""^{_90}$"""}},
        "60": {"TEXT": {"REGEX": rf"""^{_60}$"""}},
        "datum": {"ENT_TYPE": "datum"},
        "180E": {"LOWER": {"REGEX": rf"^{_180}[ew]$"}},
        "90N": {"LOWER": {"REGEX": rf"^{_90}[ns]$"}},
        "60'60": {"LOWER": {"REGEX": rf"^{_60}[{_SYM}]{_60}[{_SYM}]$"}},
        "60'60N": {"LOWER": {"REGEX": rf"^{_60}[{_SYM}]{_60}[{_SYM}][nesw]$"}},
    },
    patterns=[
        "label? 180 deg? 60 min? 60 sec? dir ,? 180 deg? 60 min? 60 sec? dir",
        "label? 180 deg? 60 min?         dir ,? 180 deg? 60 min?         dir",
        "label? 180E ,? 90N  datum?",
        "label? 90N  ,? 180E datum?",
        "label? 180 deg? 60'60  dir ,? 180 deg? 60'60  dir",
        "label? 180 deg? 60'60N     ,? 180 deg? 60'60N",
    ],
)


@registry.misc(LAT_LONG.on_match)
def on_lat_long_match(ent):
    parts = []
    for token in ent:
        if token.ent_type_ == "lat_long_label":
            continue
        if token.ent_type_ == "datum":
            ent._.data["datum"] = LAT_LONG_TERMS.replace.get(token.lower_, token.text)
        else:
            parts.append(token.text.upper())

    lat_long = " ".join(parts)
    lat_long = re.sub(rf"\s([{_PUNCT}])", r"\1", lat_long)
    ent._.data["lat_long"] = lat_long
