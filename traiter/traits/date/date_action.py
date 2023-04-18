import re
from calendar import IllegalMonthError
from datetime import date
from pathlib import Path

from dateutil import parser
from dateutil.relativedelta import relativedelta
from spacy import registry

from traiter.pipes import reject_match
from traiter.traits import terms
from traiter.traits import trait_util

DATE_MATCH = "date_match"
SHORT_DATE_MATCH = "short_date_match"

DATE_CSV = Path(__file__).parent / "date_terms.csv"
MONTH_CSV = Path(terms.__file__).parent / "month_terms.csv"

REPLACE = trait_util.term_data(MONTH_CSV, "replace")
SEP = ".,;/_'-"


@registry.misc(DATE_MATCH)
def date_match(ent):
    frags = []

    for token in ent:
        # Get the numeric parts
        if re.match(rf"^[\d{SEP}]+$", token.text):
            parts = [p for p in re.split(rf"[{SEP}]+", token.text) if p]
            if parts:
                frags += parts

        # Get a month name
        elif token._.term == "month":
            frags.append(REPLACE.get(token.lower_, token.lower_))

    # Try to parse the date
    text = " ".join(frags)
    try:
        date_ = parser.parse(text).date()
    except (parser.ParserError, IllegalMonthError):
        raise reject_match.RejectMatch()

    # Handle missing centuries like: May 22, 08
    if date_ > date.today():
        date_ -= relativedelta(years=100)
        ent._.data["century_adjust"] = True

    ent._.data["date"] = date_.isoformat()[:10]


@registry.misc(SHORT_DATE_MATCH)
def short_date_match(ent):
    date_match(ent)
    ent._.data["missing_day"] = True
    ent._.data["date"] = ent._.data["date"][:7]
