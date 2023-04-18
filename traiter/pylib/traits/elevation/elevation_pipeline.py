from spacy import Language

from . import elevation_action as act
from . import elevation_patterns as pat
from .. import add_pipe as add
from .. import trait_util

ALL_CSVS = [act.ELEVATION_CSV, act.UNIT_CSV]


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="elevation_terms", path=ALL_CSVS, **kwargs)

    prev = add.trait_pipe(
        nlp,
        name="elevation_patterns",
        compiler=pat.elevation_compilers(),
        after=prev,
    )

    prev = add.cleanup_pipe(
        nlp,
        name="elevation_cleanup",
        remove=trait_util.labels_to_remove(ALL_CSVS, keep="elevation"),
        after=prev,
    )

    return prev
