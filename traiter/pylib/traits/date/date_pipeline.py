from pathlib import Path

from spacy import Language

from .. import add_pipe as add
from .. import trait_util
from .date_custom_pipe import DATE_CUSTOM_PIPE
from .date_pattern_compilers import date_compilers


def get_csvs():
    here = Path(__file__).parent
    return [
        here / "date_terms.csv",
        here.parent / "month" / "month_terms.csv",
    ]


def build(nlp: Language, **kwargs):
    all_csvs = get_csvs()

    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name=f"date_terms", path=all_csvs, **kwargs)

    prev = add.ruler_pipe(
        nlp,
        name="date_patterns",
        compiler=date_compilers(),
        overwrite_ents=True,
        after=prev,
    )

    config = {"replace": trait_util.term_data(all_csvs, "replace")}
    prev = add.custom_pipe(nlp, DATE_CUSTOM_PIPE, config=config, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name="date_cleanup",
        remove=trait_util.labels_to_remove(all_csvs, keep="date"),
        after=prev,
    )

    return prev
