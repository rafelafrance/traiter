from pathlib import Path

from spacy import Language

from .. import add_pipe as add
from .. import trait_util
from .color_custom_pipe import COLOR_CUSTOM_PIPE
from .color_pattern_compilers import COLOR_COMPILERS

CSV = Path(__file__).parent / "color_terms.csv"


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="color_terms", path=CSV, **kwargs)

    prev = add.ruler_pipe(
        nlp,
        name="color_patterns",
        compiler=COLOR_COMPILERS,
        overwrite_ents=True,
        after=prev,
    )

    config = {
        "replace": trait_util.term_data(CSV, "replace"),
        "remove": trait_util.term_data(CSV, "remove", int),
    }
    prev = add.custom_pipe(nlp, COLOR_CUSTOM_PIPE, config=config, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name="color_cleanup",
        remove=trait_util.labels_to_remove(CSV, keep="color"),
        after=prev,
    )

    return prev
