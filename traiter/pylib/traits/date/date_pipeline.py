from pathlib import Path

from spacy import Language

from ... import add_pipe as add
from ... import trait_util
from .custom_pipe import CUSTOM_PIPE
from .pattern_compilers import COMPILERS
from .pattern_compilers import SEP

HERE = Path(__file__).parent
TRAIT = HERE.stem

CSV = HERE / f"{TRAIT}.csv"
MONTH_CSV = HERE.parent / "month" / "month.csv"


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(
            nlp,
            name=f"{TRAIT}_terms",
            path=[CSV, MONTH_CSV],
            **kwargs,
        )

    prev = add.ruler_pipe(
        nlp,
        name=f"{TRAIT}_patterns",
        compiler=COMPILERS,
        overwrite_ents=True,
        after=prev,
    )

    config = {
        "trait": TRAIT,
        "replace": trait_util.term_data(CSV, "replace"),
        "sep": SEP,
    }
    prev = add.custom_pipe(nlp, CUSTOM_PIPE, config=config, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name=f"{TRAIT}_cleanup",
        remove=trait_util.labels_to_remove([CSV, MONTH_CSV], keep=TRAIT),
        after=prev,
    )

    return prev
