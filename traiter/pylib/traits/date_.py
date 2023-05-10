import re
from calendar import IllegalMonthError
from datetime import date
from pathlib import Path

from dateutil import parser
from dateutil.relativedelta import relativedelta
from spacy.language import Language
from spacy.util import registry

from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add, reject_match

DATE_CSV = Path(__file__).parent / "terms" / "date_terms.csv"
MONTH_CSV = Path(__file__).parent / "terms" / "month_terms.csv"
NUMERIC_CSV = Path(__file__).parent / "terms" / "numeric_terms.csv"
ALL_CSVS = [DATE_CSV, MONTH_CSV, NUMERIC_CSV]

SEP = "(.,;/_'-"

REPLACE = term_util.term_data(ALL_CSVS, "replace")


def build(nlp: Language):
    add.term_pipe(nlp, name="date_terms", path=ALL_CSVS)
    add.trait_pipe(nlp, name="date_patterns", compiler=date_patterns())
    # add.debug_tokens(nlp)  # ########################################
    add.cleanup_pipe(nlp, name="date_cleanup")


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
        "roman": {"ENT_TYPE": "roman"},
    }

    return [
        Compiler(
            label="date",
            on_match="date_match",
            keep="date",
            decoder=decoder,
            patterns=[
                "label? :? 99    -* month -* 99",
                "label? :? 99    -* month -* 9999",
                "label? :? 9999  -* month -* 99",
                "label? :? 99    -* roman -* 99",
                "label? :? 99    -* roman -* 9999",
                "label? :? 9999  -* roman -* 99",
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
            on_match="missing_day_match",
            keep="date",
            decoder=decoder,
            patterns=[
                "label? :? 9999  -* month",
                "label? :? month -* 9999",
                "label? :? 99-9999",
                "label? :? 99 / 9999",
            ],
        ),
    ]


@registry.misc("date_match")
def date_match(ent):
    frags = []
    century_adjust = False

    for token in ent:

        # Get the numeric parts
        if re.match(rf"^[\d{SEP}]+$", token.text):
            parts = [p for p in re.split(rf"[{SEP}]+", token.text) if p]
            if parts:
                frags += parts

        # Get a month name
        elif token._.term in ("month", "roman"):
            frags.append(REPLACE.get(token.lower_, token.lower_))

    # Try to parse the date
    text = " ".join(frags)
    try:
        date_ = parser.parse(text).date()
    except (parser.ParserError, IllegalMonthError):
        raise reject_match.RejectMatch

    # Handle missing centuries like: May 22, 08
    if date_ > date.today():
        date_ -= relativedelta(years=100)
        century_adjust = True

    ent._.data = {
        "date": date_.isoformat()[:10],
    }
    if century_adjust:
        ent._.data["century_adjust"] = True


@registry.misc("missing_day_match")
def missing_day_match(ent):
    date_match(ent)
    ent._.data["missing_day"] = True
    ent._.data["date"] = ent._.data["date"][:7]
