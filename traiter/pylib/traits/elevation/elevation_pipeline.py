from pathlib import Path

from spacy import Language

from .. import add_pipe as add
from .. import trait_util
from .elevation_custom_pipe import ELEVATION_CUSTOM_PIPE
from .elevation_pattern_compilers import elevation_compilers


def get_csvs():
    here = Path(__file__).parent
    return [
        here / "elevation_terms.csv",
        here.parent / "units" / "unit_length_terms.csv",
    ]


def build(nlp: Language, **kwargs):
    all_csvs = get_csvs()

    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name=f"elevation_terms", path=all_csvs, **kwargs)

    prev = add.ruler_pipe(
        nlp,
        name="elevation_patterns",
        compiler=elevation_compilers(),
        overwrite_ents=True,
        after=prev,
    )

    factors_cm = trait_util.term_data(all_csvs, "factor_cm", float)
    config = {
        "replace": trait_util.term_data(all_csvs, "replace"),
        "factors_m": {k: v / 100.0 for k, v in factors_cm.items()},  # Convert to meters
    }
    prev = add.custom_pipe(nlp, ELEVATION_CUSTOM_PIPE, config=config, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name="elevation_cleanup",
        remove=trait_util.labels_to_remove(all_csvs, keep="elevation"),
        after=prev,
    )

    return prev
