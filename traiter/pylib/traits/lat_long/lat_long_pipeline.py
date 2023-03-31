from pathlib import Path

from spacy import Language

from ... import add_pipe as add
from ... import trait_util
from .custom_pipe import CUSTOM_PIPE
from .custom_pipe import CUSTOM_PIPE_UNCERTAIN
from .pattern_compilers import LAT_LONG
from .pattern_compilers import LAT_LONG_UNCERTAIN

HERE = Path(__file__).parent
TRAIT = HERE.stem

CSV = HERE / f"{TRAIT}.csv"

UNITS_DIR = HERE.parent / "units"
UNITS_CSV = UNITS_DIR / "units_length.csv"


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(
            nlp,
            name=f"{TRAIT}_terms",
            attr="lower",
            path=[CSV, UNITS_CSV],
            **kwargs,
        )

    prev = add.ruler_pipe(
        nlp,
        name=f"{TRAIT}_patterns",
        compiler=LAT_LONG,
        overwrite_ents=True,
        after=prev,
    )

    config = {"trait": TRAIT, "replace": trait_util.term_data(CSV, "replace")}
    prev = add.custom_pipe(nlp, CUSTOM_PIPE, config=config, after=prev)

    prev = add.ruler_pipe(
        nlp,
        name=f"{TRAIT}_uncertain_patterns",
        compiler=LAT_LONG_UNCERTAIN,
        overwrite_ents=True,
        after=prev,
    )

    factors_cm = trait_util.term_data(UNITS_CSV, "factor_cm", float)
    config = {
        "trait": "lat_long_uncertain",
        "replace": trait_util.term_data(CSV, "replace"),
        "factors_m": {k: v / 100.0 for k, v in factors_cm.items()},  # Convert to meters
    }
    prev = add.custom_pipe(nlp, CUSTOM_PIPE_UNCERTAIN, config=config, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name=f"{TRAIT}_cleanup",
        remove=trait_util.labels_to_remove([CSV, UNITS_CSV], keep=TRAIT),
        after=prev,
    )

    return prev
