from pathlib import Path

from spacy import Language

from .. import add_pipe as add
from .. import trait_util
from .lat_long_custom_pipe import LAT_LONG_CUSTOM_PIPE
from .lat_long_custom_pipe_untcertain import LAT_LONG_CUSTOM_PIPE_UNCERTAIN
from .lat_long_pattern_compilers import lat_long_compilers
from .lat_long_pattern_compilers import lat_long_uncertain_compilers


def get_csvs():
    here = Path(__file__).parent
    return [
        here / "lat_long_terms.csv",
        here.parent / "units" / "unit_length_terms.csv",
    ]


def build(nlp: Language, **kwargs):
    all_csvs = get_csvs()

    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="lat_long_terms", path=all_csvs, **kwargs)

    prev = add.ruler_pipe(
        nlp,
        name="lat_long_patterns",
        compiler=lat_long_compilers(),
        overwrite_ents=True,
        after=prev,
    )

    config = {"replace": trait_util.term_data(all_csvs, "replace")}
    prev = add.custom_pipe(nlp, LAT_LONG_CUSTOM_PIPE, config=config, after=prev)

    prev = add.ruler_pipe(
        nlp,
        name="lat_long_uncertain_patterns",
        compiler=lat_long_uncertain_compilers(),
        overwrite_ents=True,
        after=prev,
    )

    factors_cm = trait_util.term_data(all_csvs, "factor_cm", float)
    config = {
        "replace": trait_util.term_data(all_csvs, "replace"),
        "factors_m": {k: v / 100.0 for k, v in factors_cm.items()},  # Convert to meters
    }
    prev = add.custom_pipe(
        nlp, LAT_LONG_CUSTOM_PIPE_UNCERTAIN, config=config, after=prev
    )

    prev = add.cleanup_pipe(
        nlp,
        name="lat_long_cleanup",
        remove=trait_util.labels_to_remove(all_csvs, keep="lat_long"),
        after=prev,
    )

    return prev
