from pathlib import Path

from spacy import Language

from ... import add_pipe as add
from ... import const
from ... import trait_util

HERE = Path(__file__).parent
TRAIT = HERE.stem

FUNC = f"{TRAIT}_func"
CSV = HERE / f"{TRAIT}.csv"


def pipe(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(
            nlp,
            name=f"{TRAIT}_terms",
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
        name=f"{TRAIT}_cleanup",
        remove=trait_util.labels_to_remove(CSV, TRAIT),
        after=prev,
    )

    return prev


# ###############################################################################
REPLACE = trait_util.term_data(CSV, "replace")
REMOVE = trait_util.term_data(CSV, "remove", int)


@Language.component(FUNC)
def data_func(doc):
    for ent in [e for e in doc.ents if e.label_ == TRAIT]:
        frags = []

        for token in ent:
            # Skip anything that is not a term
            if not token._.term:
                continue

            # Skip terms marked for removal
            if REMOVE.get(token.lower_):
                continue

            # Skip names like "Brown"
            if token._.term == "color_term" and token.shape_ in const.TITLE_SHAPES:
                continue

            # Skip dashes
            if token.text in const.DASH_CHAR:
                continue

            # Color is noted as missing
            if token._.term == "color_missing":
                ent._.data["missing"] = True
                continue

            frag = REPLACE.get(token.lower_, token.lower_)

            # Skip duplicate colors within the entity
            if frag not in frags:
                frags.append(frag)

        # Build the color
        value = "-".join(frags)
        ent._.data[TRAIT] = REPLACE.get(value, value)

    return doc
