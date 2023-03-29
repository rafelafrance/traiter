from spacy import Language

from ... import add_pipe as add
from ... import trait_util
from ...const import TRAIT_DIR

HABITAT_FUNC = "habitat_data"

HERE = TRAIT_DIR / "habitat"
HABITAT_CSV = HERE / "habitat.csv"


def pipe(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.ruler_pipe(
            nlp,
            name="habitat_lower",
            attr="lower",
            path=HERE / "habitat_terms_lower.jsonl",
            **kwargs,
        )

    prev = add.ruler_pipe(
        nlp,
        name="habitat_patterns",
        path=HERE / "habitat_patterns.jsonl",
        after=prev,
        overwrite_ents=True,
    )

    prev = add.data_pipe(nlp, HABITAT_FUNC, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name="habitat_cleanup",
        remove=trait_util.labels_to_remove(HABITAT_CSV, "habitat"),
        after=prev,
    )

    return prev


# ###############################################################################
HABITAT_REPLACE = trait_util.term_data(HABITAT_CSV, "replace")


@Language.component(HABITAT_FUNC)
def habitat_data(doc):
    for ent in [e for e in doc.ents if e.label_ == "habitat"]:
        habitat_parts = []

        for token in ent:
            replaced = HABITAT_REPLACE.get(token.lower_, token.lower_)
            habitat_parts.append(replaced)

        ent._.data["habitat"] = " ".join(habitat_parts)

    return doc
