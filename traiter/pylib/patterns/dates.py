import re
from calendar import IllegalMonthError
from datetime import date

from dateutil import parser
from dateutil.relativedelta import relativedelta
from spacy.util import registry

from ..matcher_patterns import MatcherPatterns
from traiter.pylib import actions

_SEP = "[.,;/_'-]"
_LABEL_ENDER = "[:=]"
_LABELS = """ date """.split()

# ####################################################################################
_DECODER = {
    "-": {"TEXT": {"REGEX": f"^{_SEP}+$"}},
    ":": {"TEXT": {"REGEX": f"^{_LABEL_ENDER}+$"}},
    "99": {"TEXT": {"REGEX": r"^\d\d?$"}},
    "9999": {"TEXT": {"REGEX": r"^[12]\d{3}$"}},
    "label": {"LOWER": {"IN": _LABELS}},
    "month": {"ENT_TYPE": "month"},
    "99-99-9999": {"TEXT": {"REGEX": rf"^\d\d?{_SEP}+\d\d?{_SEP}+[12]\d\d\d$"}},
    "9999-99-99": {"TEXT": {"REGEX": rf"^[12]\d\d\d?{_SEP}+\d\d?{_SEP}+\d\d?$"}},
    "99-99-99": {"TEXT": {"REGEX": rf"^\d\d?{_SEP}+\d\d?{_SEP}+\d\d$"}},
    "month-99-9999": {"LOWER": {"REGEX": rf"^[a-z]+{_SEP}+\d\d?{_SEP}+[12]\d\d\d$"}},
    "99-99": {"TEXT": {"REGEX": rf"^\d\d?{_SEP}+\d\d$"}},
    "99-9999": {"TEXT": {"REGEX": rf"^\d\d?{_SEP}+[12]\d\d\d$"}},
}

# ####################################################################################
DATES = MatcherPatterns(
    name="date",
    on_match="traiter.date.v1",
    decoder=_DECODER,
    patterns=[
        "label? :? 99    -* month -* 99",
        "label? :? 99    -* month -* 9999",
        "label? :? 9999  -* month -* 99",
        "label? :? 99-99 -* 99",
        "label? :? 99-99 -* 9999",
        "label? :? 99-99-9999",
        "label? :? 99-99-99",
        "label? :? month-99-9999",
        "label? :? 9999-99-99",
        "label? :? month -* 99 -* 9999",
    ],
    output=["date"],
)


@registry.misc(DATES.on_match)
def on_date_match(ent):
    flags = re.IGNORECASE | re.VERBOSE
    text = ent.text

    text = re.sub(
        rf" ({'|'.join(_LABELS)}) \s* {_LABEL_ENDER}* \s* ",
        "",
        text,
        flags=flags,
    )
    text = re.sub(f"{_SEP}+", " ", text, flags=flags)
    try:
        date_ = parser.parse(text).date()
    except (parser.ParserError, IllegalMonthError) as err:
        raise actions.RejectMatch() from err

    if date_ > date.today():
        date_ -= relativedelta(years=100)
        ent._.data["century_adjust"] = True

    ent._.data["date"] = date_.isoformat()[:10]


# ####################################################################################
MISSING_DAYS = MatcherPatterns(
    name="short_date",
    on_match="traiter.missing_day.v1",
    decoder=_DECODER,
    patterns=[
        "label? :? 9999  -* month",
        "label? :? month -* 9999",
        "label? :? 99-9999",
        # "label? :? 99-99",
        # "label? :? 9     -* 99",
        # "label? :? 99    -* 9",
        # "label? :? 9     -* 9999",
        # "label? :? month -* 99",
        # "label? :? 9999  -* 9",
    ],
    output=["date"],
)


@registry.misc(MISSING_DAYS.on_match)
def on_missing_day_match(ent):
    flags = re.IGNORECASE | re.VERBOSE
    if re.match(r"\d\d? [\s'] \d\d?", ent.text, flags=flags):
        raise actions.RejectMatch()

    on_date_match(ent)
    ent._.data["date"] = ent._.data["date"][:7]
    ent._.data["missing_day"] = True
    ent._.new_label = "date"
