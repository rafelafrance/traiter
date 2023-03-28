from spacy import Language

from .. import util
from ..common import PATTERN_DIR

HERE = PATTERN_DIR / "elevation"
UNITS = PATTERN_DIR / "units_length"


def pipe(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = util.ruler_pipe(
            nlp,
            name="elev_lower",
            attr="lower",
            path=HERE / "elevation_terms_lower.jsonl",
            **kwargs,
        )
        prev = util.ruler_pipe(
            nlp,
            name="elev_units",
            attr="lower",
            path=UNITS / "units_length_terms_lower.jsonl",
            after=prev,
        )

    prev = util.ruler_pipe(
        nlp,
        name="elev_patterns",
        path=HERE / "elevation_patterns.jsonl",
        after=prev,
        overwrite_ents=True,
    )
    prev = util.cleanup_pipe(
        nlp, name="elev_cleanup", cleanup=["elev_label"], after=prev
    )

    return prev
