from spacy import Language

from .. import add
from junk.common import PATTERN_DIR

HERE = PATTERN_DIR / "color"


def pipe(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.ruler_pipe(
            nlp,
            name="color_month",
            attr="lower",
            path=HERE / "color_terms_lower.jsonl",
            **kwargs,
        )

    prev = add.ruler_pipe(
        nlp,
        name="color_patterns",
        path=HERE / "color_patterns.jsonl",
        after=prev,
        overwrite_ents=True,
    )
    prev = add.cleanup_pipe(
        nlp, name="color_cleanup", cleanup=["color_mod", "color_term"], after=prev
    )

    return prev
