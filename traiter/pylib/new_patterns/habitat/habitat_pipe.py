from spacy import Language

from .. import util
from ..common import PATTERN_DIR

HERE = PATTERN_DIR / "habitat"


def pipe(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = util.ruler_pipe(
            nlp,
            name="habitat_lower",
            attr="lower",
            path=HERE / "habitat_terms_lower.jsonl",
            **kwargs,
        )

    prev = util.ruler_pipe(
        nlp,
        name="habitat_patterns",
        path=HERE / "habitat_patterns.jsonl",
        after=prev,
        overwrite_ents=True,
    )
    prev = util.cleanup_pipe(
        nlp,
        name="habitat_cleanup",
        cleanup=["habitat_term", "habitat_prefix", "habitat_suffix", "not_habitat"],
        after=prev,
    )

    return prev
