from spacy import Language

from .. import add_pipe as add
from .. import trait_util
from .lat_long_action import LAT_LONG_CSV
from .lat_long_action import UNIT_CSV
from .lat_long_patterns import lat_long_compilers
from .lat_long_patterns import lat_long_uncertain_compilers


ALL_CSVS = [LAT_LONG_CSV, UNIT_CSV]


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="lat_long_terms", path=ALL_CSVS, **kwargs)

    prev = add.trait_pipe(
        nlp,
        name="lat_long_patterns",
        compiler=lat_long_compilers(),
        after=prev,
    )

    prev = add.trait_pipe(
        nlp,
        name="lat_long_uncertain_patterns",
        compiler=lat_long_uncertain_compilers(),
        after=prev,
    )

    prev = add.cleanup_pipe(
        nlp,
        name="lat_long_cleanup",
        remove=trait_util.labels_to_remove(ALL_CSVS, keep="lat_long"),
        after=prev,
    )

    return prev
