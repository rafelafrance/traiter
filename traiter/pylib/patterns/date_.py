import re
from calendar import IllegalMonthError
from datetime import date

from dateutil import parser
from dateutil.relativedelta import relativedelta
from spacy.util import registry

from traiter.pylib import actions
from traiter.pylib.pattern_compilers.matcher import Compiler
from traiter.pylib.term_list import TermList

DATE_TERMS = TermList.pick_shared("time", "month")

_SEPARATOR = r"[.,;/_'-]"
_COMMA = r"[.,/_-]"
_LABEL_ENDER = r"[:=]"
_LABELS = """ date """.split()


# ####################################################################################
_DECODER = {
    "-": {"TEXT": {"REGEX": f"^{_SEPARATOR}+$"}},
    ":": {"TEXT": {"REGEX": f"^{_LABEL_ENDER}+$"}},
    "9": {"TEXT": {"REGEX": r"^\d\d?$"}},
    "99": {"TEXT": {"REGEX": r"^\d\d$"}},
    "label": {"LOWER": {"IN": _LABELS}},
    "month": {"ENT_TYPE": "month"},
    "9999": {"TEXT": {"REGEX": r"^[12]\d{3}$"}},
}


# ####################################################################################
DATE = Compiler(
    "date",
    on_match="traiter.date.v1",
    decoder=_DECODER,
    patterns=[
        "label? :? 9     -* 9     -* 9",
        "label? :? 9     -* 9     -* 9999",
        "label? :? 9     -* month -* 9",
        "label? :? 9     -* month -* 9999",
        "label? :? month -* 9     -* 9",
        "label? :? month -* 9     -* 9999",
        "label? :? 9999  -* 9     -* 9",
        "label? :? 9999  -* month -* 9",
    ],
)


@registry.misc(DATE.on_match)
def on_date_match(ent):
    flags = re.IGNORECASE | re.VERBOSE
    text = ent.text

    if re.match(r"\d\d? \s \d\d? \s \d\d?", text, flags=flags):
        raise actions.RejectMatch()

    text = re.sub(
        rf" ({'|'.join(_LABELS)}) \s* {_LABEL_ENDER}* \s* ",
        "",
        text,
        flags=flags,
    )
    text = re.sub(f"{_COMMA}+", " ", text, flags=flags)
    try:
        date_ = parser.parse(text).date()
    except (parser.ParserError, IllegalMonthError) as err:
        raise actions.RejectMatch() from err

    if date_ > date.today():
        date_ -= relativedelta(years=100)
        ent._.data["century_adjust"] = True

    ent._.data["date"] = date_.isoformat()[:10]


# ####################################################################################
MISSING_DAY = Compiler(
    "short_date",
    on_match="traiter.missing_day.v1",
    decoder=_DECODER,
    patterns=[
        "label? :? 9     -* 99",
        "label? :? 99    -* 9",
        "label? :? 9     -* 9999",
        "label? :? month -* 9999",
        "label? :? month -* 99",
        "label? :? 9999  -* 9",
        "label? :? 9999  -* month",
    ],
)


@registry.misc(MISSING_DAY.on_match)
def short_date(ent):
    flags = re.IGNORECASE | re.VERBOSE
    if re.match(r"\d\d? [\s'] \d\d?", ent.text, flags=flags):
        raise actions.RejectMatch()

    on_date_match(ent)
    ent._.data["date"] = ent._.data["date"][:7]
    ent._.data["missing_day"] = True
    ent._.new_label = "date"
