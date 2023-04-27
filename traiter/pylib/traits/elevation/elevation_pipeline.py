from spacy.language import Language

from . import elevation_action as act
from . import elevation_patterns as pat
from .. import add_pipe as add


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="elevation_terms", path=act.ALL_CSVS, **kwargs)

    prev = add.trait_pipe(
        nlp,
        name="elevation_patterns",
        compiler=pat.elevation_compilers(),
        after=prev,
    )

    # prev = add.debug_tokens(nlp, after=prev)  # #############################

    prev = add.cleanup_pipe(nlp, name="elevation_cleanup", after=prev)

    return prev
