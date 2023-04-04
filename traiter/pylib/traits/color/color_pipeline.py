from pathlib import Path

from spacy import Language

from .. import add_pipe as add
from .. import trait_util
from .color_custom_pipe import COLOR_CUSTOM_PIPE
from .color_pattern_compilers import color_compilers


def build(nlp: Language, **kwargs):
    color_csv = Path(__file__).parent / "color_terms.csv"

    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="color_terms", path=color_csv, **kwargs)

    prev = add.ruler_pipe(
        nlp,
        name="color_patterns",
        compiler=color_compilers(),
        overwrite_ents=True,
        after=prev,
    )

    config = {
        "replace": trait_util.term_data(color_csv, "replace"),
        "remove": trait_util.term_data(color_csv, "remove", int),
    }
    prev = add.custom_pipe(nlp, COLOR_CUSTOM_PIPE, config=config, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name="color_cleanup",
        remove=trait_util.labels_to_remove(color_csv, keep="color"),
        after=prev,
    )

    return prev
