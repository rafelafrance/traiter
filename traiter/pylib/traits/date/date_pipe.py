from spacy import Language

from .. import add
from junk.common import PATTERN_DIR

HERE = PATTERN_DIR / "date"
MONTH = PATTERN_DIR / "month"


def pipe(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.ruler_pipe(
            nlp,
            name="date_month",
            attr="lower",
            path=MONTH / "month_terms_lower.jsonl",
            **kwargs,
        )
        prev = add.ruler_pipe(
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
    prev = add.cleanup_pipe(nlp, name="date_cleanup", cleanup=["month"], after=prev)

    return prev
