from spacy.language import Language

from . import lat_long_action as act
from . import lat_long_patterns as pat
from .. import add_pipe as add

ALL_CSVS = [act.LAT_LONG_CSV, act.UNIT_CSV]


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="lat_long_terms", path=ALL_CSVS, **kwargs)

    # prev = add.debug_tokens(nlp, after=prev)  # ##################################

    prev = add.trait_pipe(
        nlp,
        name="lat_long_patterns",
        compiler=pat.lat_long_compilers(),
        after=prev,
    )

    # prev = add.debug_tokens(nlp, after=prev)  # ##################################

    prev = add.trait_pipe(
        nlp,
        name="lat_long_uncertain_patterns",
        compiler=pat.lat_long_uncertain_compilers(),
        after=prev,
    )

    prev = add.cleanup_pipe(nlp, name="lat_long_cleanup", after=prev)

    return prev
