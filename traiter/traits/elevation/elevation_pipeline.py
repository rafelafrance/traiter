from spacy import Language

from .. import add_pipe as add
from .. import trait_util
from .elevation_action import ELEVATION_CSV
from .elevation_action import UNIT_CSV
from .elevation_patterns import elevation_compilers

ALL_CSVS = [ELEVATION_CSV, UNIT_CSV]


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name=f"elevation_terms", path=ALL_CSVS, **kwargs)

    prev = add.trait_pipe(
        nlp,
        name="elevation_patterns",
        compiler=elevation_compilers(),
        after=prev,
    )

    prev = add.cleanup_pipe(
        nlp,
        name="elevation_cleanup",
        remove=trait_util.labels_to_remove(ALL_CSVS, keep="elevation"),
        after=prev,
    )

    return prev
