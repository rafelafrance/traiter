from pathlib import Path

from spacy import Language

from .. import add_pipe as add
from .. import trait_util
from .lat_long_custom_pipe import LAT_LONG_CUSTOM_PIPE
from .lat_long_custom_pipe_untcertain import LAT_LONG_CUSTOM_PIPE_UNCERTAIN
from .lat_long_pattern_compilers import LAT_LONG
from .lat_long_pattern_compilers import LAT_LONG_UNCERTAIN

HERE = Path(__file__).parent

CSV = HERE / "lat_long_terms.csv"
UNITS_CSV = HERE.parent / "units" / "unit_length_terms.csv"
ALL_CSVS = [CSV, UNITS_CSV]


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="lat_long_terms", path=ALL_CSVS, **kwargs)

    prev = add.ruler_pipe(
        nlp,
        name="lat_long_patterns",
        compiler=LAT_LONG,
        overwrite_ents=True,
        after=prev,
    )

    config = {"replace": trait_util.term_data(CSV, "replace")}
    prev = add.custom_pipe(nlp, LAT_LONG_CUSTOM_PIPE, config=config, after=prev)

    prev = add.ruler_pipe(
        nlp,
        name="lat_long_uncertain_patterns",
        compiler=LAT_LONG_UNCERTAIN,
        overwrite_ents=True,
        after=prev,
    )

    factors_cm = trait_util.term_data(UNITS_CSV, "factor_cm", float)
    config = {
        "replace": trait_util.term_data(ALL_CSVS, "replace"),
        "factors_m": {k: v / 100.0 for k, v in factors_cm.items()},  # Convert to meters
    }
    prev = add.custom_pipe(
        nlp, LAT_LONG_CUSTOM_PIPE_UNCERTAIN, config=config, after=prev
    )

    prev = add.cleanup_pipe(
        nlp,
        name="lat_long_cleanup",
        remove=trait_util.labels_to_remove(ALL_CSVS, keep="lat_long"),
        after=prev,
    )

    return prev
