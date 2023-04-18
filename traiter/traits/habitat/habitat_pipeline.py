from spacy import Language

from .habitat_action import HABITAT_CSV
from .habitat_patterns import habitat_compilers
from traiter.traits import add_pipe as add
from traiter.traits import trait_util


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="habitat_terms", path=HABITAT_CSV, **kwargs)

    prev = add.trait_pipe(
        nlp,
        name="habitat_patterns",
        compiler=habitat_compilers(),
        after=prev,
    )

    prev = add.cleanup_pipe(
        nlp,
        name="habitat_cleanup",
        remove=trait_util.labels_to_remove(HABITAT_CSV, keep="habitat"),
        after=prev,
    )

    return prev
