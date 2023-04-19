from spacy.language import Language

from . import date_action as act
from . import date_patterns as pat
from .. import add_pipe as add
from .. import trait_util

ALL_CSVS = [act.DATE_CSV, act.MONTH_CSV]


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="date_terms", path=ALL_CSVS, **kwargs)

    prev = add.trait_pipe(
        nlp,
        name="date_patterns",
        compiler=pat.date_patterns(),
        after=prev,
    )

    prev = add.cleanup_pipe(
        nlp,
        name="date_cleanup",
        remove=trait_util.labels_to_remove(ALL_CSVS, keep="date"),
        after=prev,
    )

    return prev
