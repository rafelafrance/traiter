from spacy import Language

from .date_action import DATE_CSV
from .date_action import MONTH_CSV
from .date_patterns import date_patterns
from traiter.traits import add_pipe as add
from traiter.traits import trait_util

ALL_CSVS = [DATE_CSV, MONTH_CSV]


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="date_terms", path=ALL_CSVS, **kwargs)

    prev = add.trait_pipe(
        nlp,
        name="date_patterns",
        compiler=date_patterns(),
        after=prev,
    )

    prev = add.cleanup_pipe(
        nlp,
        name="date_cleanup",
        remove=trait_util.labels_to_remove(ALL_CSVS, keep="date"),
        after=prev,
    )

    return prev
