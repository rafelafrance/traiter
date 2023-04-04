from pathlib import Path

from spacy import Language

from .. import add_pipe as add
from .. import trait_util
from .habitat_custom_pipe import HABITAT_CUSTOM_PIPE
from .habitat_pattern_compilers import habitat_compilers


def build(nlp: Language, **kwargs):
    habitat_csv = Path(__file__).parent / "habitat_terms.csv"

    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="habitat_terms", path=habitat_csv, **kwargs)

    prev = add.ruler_pipe(
        nlp,
        name="habitat_patterns",
        compiler=habitat_compilers(),
        overwrite_ents=True,
        after=prev,
    )

    config = {"replace": trait_util.term_data(habitat_csv, "replace")}
    prev = add.custom_pipe(nlp, HABITAT_CUSTOM_PIPE, config=config, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name="habitat_cleanup",
        remove=trait_util.labels_to_remove(habitat_csv, keep="habitat"),
        after=prev,
    )

    return prev
