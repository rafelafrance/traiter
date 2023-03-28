from spacy import Language

from .. import add
from junk.common import PATTERN_DIR

HERE = PATTERN_DIR / "elevation"
UNITS = PATTERN_DIR / "units_length"


def pipe(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.ruler_pipe(
            nlp,
            name="elev_lower",
            attr="lower",
            path=HERE / "elevation_terms_lower.jsonl",
            **kwargs,
        )
        prev = add.ruler_pipe(
            nlp,
            name="elev_units",
            attr="lower",
            path=UNITS / "units_length_terms_lower.jsonl",
            after=prev,
        )

    prev = add.ruler_pipe(
        nlp,
        name="elev_patterns",
        path=HERE / "elevation_patterns.jsonl",
        after=prev,
        overwrite_ents=True,
    )
    prev = add.cleanup_pipe(
        nlp, name="elev_cleanup", cleanup=["elev_label"], after=prev
    )

    return prev
