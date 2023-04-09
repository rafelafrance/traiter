from spacy import Language

from .. import add_pipe as add
from .. import trait_util
from .color_action import COLOR_CSV
from .color_patterns import color_patterns


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="color_terms", path=COLOR_CSV, **kwargs)

    prev = add.trait_pipe(
        nlp,
        name="color_patterns",
        compiler=color_patterns(),
        after=prev,
    )

    prev = add.cleanup_pipe(
        nlp,
        name="color_cleanup",
        remove=trait_util.labels_to_remove(COLOR_CSV, keep="color"),
        after=prev,
    )

    return prev
