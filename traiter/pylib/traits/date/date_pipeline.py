from pathlib import Path

from spacy import Language

from .. import add_pipe as add
from .. import trait_util
from .date_custom_pipe import DATE_CUSTOM_PIPE
from .date_pattern_compilers import DATE_COMPILERS

HERE = Path(__file__).parent

CSV = HERE / "date_terms.csv"
MONTH_CSV = HERE.parent / "month" / "month_terms.csv"
ALL_CSVS = [CSV, MONTH_CSV]


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name=f"date_terms", path=ALL_CSVS, **kwargs)

    prev = add.ruler_pipe(
        nlp,
        name="date_patterns",
        compiler=DATE_COMPILERS,
        overwrite_ents=True,
        after=prev,
    )

    config = {"replace": trait_util.term_data(ALL_CSVS, "replace")}
    prev = add.custom_pipe(nlp, DATE_CUSTOM_PIPE, config=config, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name="date_cleanup",
        remove=trait_util.labels_to_remove(ALL_CSVS, keep="date"),
        after=prev,
    )

    return prev
