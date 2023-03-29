from spacy import Language

from .. import add
from .. import trait_util
from ... import const

COLOR_FUNC = "color_data"

HERE = const.TRAIT_DIR / "color"
COLOR_CSV = HERE / "color.csv"


def pipe(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(
            nlp,
            name="color_terms",
            attr="lower",
            path=HERE / "color_terms_lower.jsonl",
            **kwargs,
        )

    prev = add.ruler_pipe(
        nlp,
        name="color_patterns",
        path=HERE / "color_patterns.jsonl",
        after=prev,
        overwrite_ents=True,
    )

    prev = add.data_pipe(nlp, COLOR_FUNC, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name="color_cleanup",
        remove=trait_util.labels_to_remove(COLOR_CSV, "color"),
        after=prev,
    )

    return prev


# ###############################################################################
COLOR_REPLACE = trait_util.term_data(COLOR_CSV, "replace")
COLOR_REMOVE = trait_util.term_data(COLOR_CSV, "remove", int)

FIX_DASHES = ["\\" + c for c in const.DASH_CHAR]
FIX_DASHES = "".join(FIX_DASHES)
FIX_DASHES = rf"[{FIX_DASHES}]{{2,}}|[{FIX_DASHES}]$"


@Language.component(COLOR_FUNC)
def color_data(doc):
    for ent in [e for e in doc.ents if e.label_ == "color"]:
        color_parts = []

        for token in ent:
            # Skip anything that is not a term
            if not token._.term:
                continue

            # Skip terms marked for removal
            if COLOR_REMOVE.get(token.lower_):
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

            replace = COLOR_REPLACE.get(token.lower_, token.lower_)

            # Skip duplicate colors within the entity
            if replace not in color_parts:
                color_parts.append(replace)

        # Build the color
        value = "-".join(color_parts)
        ent._.data["color"] = COLOR_REPLACE.get(value, value)

    return doc
