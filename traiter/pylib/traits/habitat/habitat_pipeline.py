from spacy.language import Language

from . import habitat_action as act
from . import habitat_patterns as pat
from .. import add_pipe as add
from .. import trait_util


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="habitat_terms", path=act.HABITAT_CSV, **kwargs)

    # prev = add.debug_tokens(nlp, after=prev)  # ##############################

    prev = add.trait_pipe(
        nlp,
        name="habitat_patterns",
        compiler=pat.habitat_compilers(),
        after=prev,
    )

    prev = add.cleanup_pipe(
        nlp,
        name="habitat_cleanup",
        remove=trait_util.labels_to_remove(act.HABITAT_CSV, keep="habitat"),
        after=prev,
    )

    return prev
