from spacy import Language

from .. import util
from ..common import PATTERN_DIR

HERE = PATTERN_DIR / "lat_long"
UNITS = PATTERN_DIR / "units_distance"


def pipe(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = util.ruler_pipe(
            nlp,
            name="lat_long_lower",
            attr="lower",
            path=HERE / "lat_long_terms_lower.jsonl",
            **kwargs,
        )
        prev = util.ruler_pipe(
            nlp,
            name="lat_long_units",
            attr="lower",
            path=UNITS / "units_distance_terms_lower.jsonl",
            after=prev,
        )

    prev = util.ruler_pipe(
        nlp,
        name="lat_long_patterns",
        path=HERE / "lat_long_patterns.jsonl",
        after=prev,
        overwrite_ents=True,
    )
    prev = util.ruler_pipe(
        nlp,
        name="lat_long_uncertain_patterns",
        path=HERE / "lat_long_uncertain_patterns.jsonl",
        after=prev,
        overwrite_ents=True,
    )
    util.cleanup_pipe(
        nlp,
        name="lat_long_cleanup",
        cleanup=[
            "datum",
            "lat_long_label",
            "uncertain_label",
            "metric_dist",
            "imperial_dist",
        ],
        after=prev,
    )

    return prev
