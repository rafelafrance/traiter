from pathlib import Path

from spacy import Language

from .. import add_pipe as add
from .. import trait_util
from .elevation_custom_pipe import ELEVATION_CUSTOM_PIPE
from .elevation_pattern_compilers import ELEVATION_COMPILERS

HERE = Path(__file__).parent

CSV = HERE / "elevation_terms.csv"
UNITS_CSV = HERE.parent / "units" / "unit_length_terms.csv"
ALL_CSVS = [CSV, UNITS_CSV]


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name=f"elevation_terms", path=ALL_CSVS, **kwargs)

    prev = add.ruler_pipe(
        nlp,
        name="elevation_patterns",
        compiler=ELEVATION_COMPILERS,
        overwrite_ents=True,
        after=prev,
    )

    factors_cm = trait_util.term_data(UNITS_CSV, "factor_cm", float)
    config = {
        "replace": trait_util.term_data(ALL_CSVS, "replace"),
        "factors_m": {k: v / 100.0 for k, v in factors_cm.items()},  # Convert to meters
    }
    prev = add.custom_pipe(nlp, ELEVATION_CUSTOM_PIPE, config=config, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name="elevation_cleanup",
        remove=trait_util.labels_to_remove(ALL_CSVS, keep="elevation"),
        after=prev,
    )

    return prev
