from spacy.language import Language

from . import color_action as act
from . import color_patterns as pat
from .. import add_pipe as add


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="color_terms", path=act.COLOR_CSV, **kwargs)

    prev = add.trait_pipe(
        nlp,
        name="color_patterns",
        compiler=pat.color_patterns(),
        after=prev,
    )

    prev = add.cleanup_pipe(nlp, name="color_cleanup", after=prev)

    return prev
