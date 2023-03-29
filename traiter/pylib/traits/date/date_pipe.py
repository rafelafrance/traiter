import re
from calendar import IllegalMonthError
from datetime import date
from pathlib import Path

from dateutil import parser
from dateutil.relativedelta import relativedelta
from spacy import Language

from ... import add_pipe as add
from ... import trait_util
from .date_compilers import SEP

HERE = Path(__file__).parent
TRAIT = HERE.stem

FUNC = f"{TRAIT}_func"
CSV = HERE / f"{TRAIT}.csv"

MONTH = HERE.parent / "month"
MONTH_CSV = MONTH / "month.csv"


def pipe(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(
            nlp,
            name=f"{TRAIT}_terms",
            attr="lower",
            path=HERE / f"{TRAIT}_terms_lower.jsonl",
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
        name=f"{TRAIT}_patterns",
        path=HERE / f"{TRAIT}_patterns.jsonl",
        after=prev,
        overwrite_ents=True,
    )

    prev = add.data_pipe(nlp, FUNC, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name="date_cleanup",
        remove=trait_util.labels_to_remove([CSV, MONTH_CSV], TRAIT),
        after=prev,
    )

    return prev


# ###############################################################################
REPLACE = trait_util.term_data(CSV, "replace")


@Language.component(FUNC)
def data_func(doc):
    for ent in [e for e in doc.ents if e.label_ == TRAIT]:
        frags = []

        for token in ent:
            # Get the numeric parts
            if re.match(rf"^[\d{SEP}]+$", token.text):
                date_parts = [p for p in re.split(rf"[{SEP}]+", token.text) if p]
                if date_parts:
                    frags += date_parts

            # Get a month name
            elif token._.term == "month":
                frags.append(REPLACE.get(token.lower_, token.lower_))

        # Try to parse the date
        text = " ".join(frags)
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
