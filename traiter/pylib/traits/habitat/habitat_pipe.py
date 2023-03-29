from pathlib import Path

from spacy import Language

from ... import add_pipe as add
from ... import trait_util

HERE = Path(__file__).parent
TRAIT = HERE.stem

FUNC = f"{TRAIT}_func"
CSV = HERE / f"{TRAIT}.csv"


def pipe(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.ruler_pipe(
            nlp,
            name=f"{TRAIT}_lower",
            attr="lower",
            path=HERE / f"{TRAIT}_terms_lower.jsonl",
            **kwargs,
        )

    prev = add.ruler_pipe(
        nlp,
        name=f"{TRAIT}_patterns",
        path=HERE / f"{TRAIT}_patterns.jsonl",
        after=prev,
        overwrite_ents=True,
    )

    prev = add.data_pipe(nlp, FUNC, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name="habitat_cleanup",
        remove=trait_util.labels_to_remove(CSV, TRAIT),
        after=prev,
    )

    return prev


# ###############################################################################
REPLACE = trait_util.term_data(CSV, "replace")


@Language.component(FUNC)
def data_func(doc):
    for ent in [e for e in doc.ents if e.label_ == TRAIT]:
        frags = []

        for token in ent:
            replaced = REPLACE.get(token.lower_, token.lower_)
            frags.append(replaced)

        ent._.data["habitat"] = " ".join(frags)

    return doc
