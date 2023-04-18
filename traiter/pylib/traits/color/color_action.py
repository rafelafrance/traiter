from pathlib import Path

from spacy import registry

from traiter.pylib import const
from traiter.pylib.traits import trait_util

COLOR_MATCH = "color_match"

COLOR_CSV = Path(__file__).parent / "color_terms.csv"

REPLACE = trait_util.term_data(COLOR_CSV, "replace")
REMOVE = trait_util.term_data(COLOR_CSV, "remove", int)


@registry.misc(COLOR_MATCH)
def color_match(ent):
    frags = []

    for token in ent:
        # Skip anything that is not a term
        if not token._.term:
            continue

        # Skip terms marked for removal
        if REMOVE.get(token.lower_):
            continue

        # Skip names like "Brown"
        if token._.term == "color" and token.shape_ in const.TITLE_SHAPES:
            continue

        # Skip dashes
        if token.text in const.DASH:
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
    ent._.data["color"] = REPLACE.get(value, value)
