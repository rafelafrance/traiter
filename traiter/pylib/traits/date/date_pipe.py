import re
from calendar import IllegalMonthError
from datetime import date

from dateutil import parser
from dateutil.relativedelta import relativedelta
from spacy import Language

from ... import add_pipe as add
from ... import trait_util
from ...const import TRAIT_DIR
from .date_compilers import SEP

TRAIT = "date"
DATE_FUNC = f"{TRAIT}_data"

HERE = TRAIT_DIR / "date"
DATE_CSV = HERE / "date.csv"

MONTH = TRAIT_DIR / "month"
MONTH_CSV = MONTH / "month.csv"


def pipe(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(
            nlp,
            name="date_terms",
            attr="lower",
            path=HERE / "date_terms_lower.jsonl",
            **kwargs,
        )

        prev = add.term_pipe(
            nlp,
            name="date_month",
            attr="lower",
            path=MONTH / "month_terms_lower.jsonl",
            after=prev,
        )

        prev = add.term_pipe(
            nlp,
            name="month_text",
            attr="text",
            path=MONTH / "month_terms_text.jsonl",
            after=prev,
        )

    prev = add.ruler_pipe(
        nlp,
        name="date_patterns",
        path=HERE / "date_patterns.jsonl",
        after=prev,
        overwrite_ents=True,
    )

    prev = add.data_pipe(nlp, DATE_FUNC, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name="date_cleanup",
        remove=trait_util.labels_to_remove([DATE_CSV, MONTH_CSV], "date"),
        after=prev,
    )

    return prev


# ###############################################################################
DATE_REPLACE = trait_util.term_data(DATE_CSV, "replace")


@Language.component(DATE_FUNC)
def date_data(doc):
    for ent in [e for e in doc.ents if e.label_ == "date"]:
        date_parts = []

        for token in ent:
            # Get the numeric parts
            if re.match(rf"^[\d{SEP}]+$", token.text):
                parts = [p for p in re.split(rf"[{SEP}]+", token.text) if p]
                if parts:
                    date_parts += parts

            # Get a month name
            elif token._.term == "month":
                date_parts.append(DATE_REPLACE.get(token.lower_, token.lower_))

        # Try to parse the date
        text = " ".join(date_parts)
        try:
            date_ = parser.parse(text).date()
        except (parser.ParserError, IllegalMonthError):
            ent._.delete = True
            return

        # Handle missing centuries like: May 22, 08
        if date_ > date.today():
            date_ -= relativedelta(years=100)
            ent._.data["century_adjust"] = True

        ent._.data["date"] = date_.isoformat()[:10]
        if ent.id_ == "short_date":
            ent._.data["missing_day"] = True
            ent._.data["date"] = date_.isoformat()[:7]

    return doc
