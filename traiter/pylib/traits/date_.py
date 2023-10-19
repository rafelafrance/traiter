import re
from calendar import IllegalMonthError
from datetime import date as dt
from pathlib import Path

from dateutil import parser
from dateutil.relativedelta import relativedelta
from spacy.language import Language
from spacy.util import registry

from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add, reject_match

from .base import Base


class Date(Base):
    date_csv = Path(__file__).parent / "terms" / "date_terms.csv"
    month_csv = Path(__file__).parent / "terms" / "month_terms.csv"
    numeric_csv = Path(__file__).parent / "terms" / "numeric_terms.csv"
    all_csvs = [date_csv, month_csv, numeric_csv]

    sep = "(.,;/_'-"

    replace = term_util.term_data(all_csvs, "replace")

    def __init__(
        self,
        trait: str = None,
        start: int = None,
        end: int = None,
        date: str = None,
        century_adjust: bool = None,
        missing_day: bool = None,
    ):
        super().__init__(trait, start, end)
        self.date = date
        self.century_adjust = century_adjust
        self.missing_day = missing_day

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="date_terms", path=cls.all_csvs)
        add.trait_pipe(nlp, name="date_patterns", compiler=cls.date_patterns())
        add.cleanup_pipe(nlp, name="date_cleanup")

    @classmethod
    def date_patterns(cls):
        decoder = {
            "-": {"TEXT": {"REGEX": rf"^[{cls.sep}]\Z"}},
            "/": {"TEXT": {"REGEX": r"^/\Z"}},
            "99": {"TEXT": {"REGEX": r"^\d\d?\Z"}},
            "99-99": {"TEXT": {"REGEX": rf"^\d\d?[{cls.sep}]+\d\d\Z"}},
            "99-9999": {"TEXT": {"REGEX": rf"^\d\d?[{cls.sep}]+[12]\d\d\d\Z"}},
            "9999": {"TEXT": {"REGEX": r"^[12]\d{3}\Z"}},
            ":": {"TEXT": {"REGEX": r"^[:=]+\Z"}},
            "label": {"ENT_TYPE": "date_label"},
            "month": {"ENT_TYPE": "month"},
            "roman": {"ENT_TYPE": "roman"},
        }

        return [
            Compiler(
                label="date",
                on_match="date_trait",
                keep="date",
                decoder=decoder,
                patterns=[
                    "label? :? 99     -* month -* 99",
                    "label? :? 99     -* month -* 9999",
                    "label? :? 9999   -* month -* 99",
                    "label? :? 99     -* roman -* 99",
                    "label? :? 99     -* roman -* 9999",
                    "label? :? 9999   -* roman -* 99",
                    "label? :? 99     -  99    -  99",
                    "label? :? 99     -  99    -  9999",
                    "label? :? month+ -* 99    -* 9999",
                    "label? :? 9999   -  99    -  99",
                    "label? :? month+ -* 99-9999",
                    "label? :? month+ -* 99-99",
                ],
            ),
            Compiler(
                label="short_date",
                id="date",
                on_match="short_date_match",
                keep="date",
                decoder=decoder,
                patterns=[
                    "label? :? 9999   -* month",
                    "label? :? 9999   -* roman",
                    "label? :? month+ -* 9999",
                    "label? :? roman+ -* 9999",
                    "label? :? 99-9999",
                    "label? :? 99 / 9999",
                ],
            ),
        ]

    @classmethod
    def date_trait(cls, ent):
        frags = []
        century_adjust = None

        for token in ent:
            # Get the numeric parts
            if re.match(rf"^[\d{cls.sep}]+$", token.text):
                parts = [p for p in re.split(rf"[{cls.sep}]+", token.text) if p]
                if parts:
                    frags += parts

            # Get a month name
            elif token._.term in ("month", "roman"):
                month = cls.replace.get(
                    token.text, cls.replace.get(token.lower_, token.lower_)
                )
                frags.append(month)

        # Try to parse the date
        text = " ".join(frags)
        try:
            date_ = parser.parse(text).date()
        except (parser.ParserError, IllegalMonthError):
            raise reject_match.RejectMatch

        # Handle missing centuries like: May 22, 08
        if date_ > dt.today():
            date_ -= relativedelta(years=100)
            century_adjust = True

        date_ = date_.isoformat()[:10]

        return super().from_ent(
            ent, date=date_, century_adjust=century_adjust, missing_day=None
        )

    @classmethod
    def short_date(cls, ent):
        date_ = Date.date_trait(ent)
        date_.trait = "date"
        date_.missing_day = True
        date_.date = date_.date[:7]
        return date_


@registry.misc("date_trait")
def date_match(ent):
    return Date.date_trait(ent)


@registry.misc("short_date_match")
def short_date_match(ent):
    return Date.short_date(ent)
