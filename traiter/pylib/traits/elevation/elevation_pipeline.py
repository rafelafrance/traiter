from pathlib import Path

from spacy import Language

from .. import add_pipe as add
from .. import trait_util
from .custom_pipe import CUSTOM_PIPE
from .pattern_compilers import COMPILERS

HERE = Path(__file__).parent
TRAIT = HERE.stem

CSV = HERE / "elevation.csv"
UNITS_CSV = HERE.parent / "units" / "units_length.csv"

ALL_CSVS = [CSV, UNITS_CSV]


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name=f"{TRAIT}_terms", path=ALL_CSVS, **kwargs)

    prev = add.ruler_pipe(
        nlp,
        name=f"{TRAIT}_patterns",
        compiler=COMPILERS,
        overwrite_ents=True,
        after=prev,
    )

    factors_cm = trait_util.term_data(UNITS_CSV, "factor_cm", float)
    config = {
        "trait": TRAIT,
        "replace": trait_util.term_data(ALL_CSVS, "replace"),
        "factors_m": {k: v / 100.0 for k, v in factors_cm.items()},  # Convert to meters
    }
    prev = add.custom_pipe(nlp, CUSTOM_PIPE, config=config, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name=f"{TRAIT}_cleanup",
        remove=trait_util.labels_to_remove(ALL_CSVS, keep=TRAIT),
        after=prev,
    )

    return prev
