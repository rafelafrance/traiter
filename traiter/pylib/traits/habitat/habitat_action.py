from pathlib import Path

from spacy.util import registry

from traiter.pylib.traits import trait_util

HABITAT_MATCH = "habitat_match"
LABELED_HABITAT_MATCH = "labeld_habitat_match"

HABITAT_CSV = Path(__file__).parent / "habitat_terms.csv"

REPLACE = trait_util.term_data(HABITAT_CSV, "replace")


@registry.misc(HABITAT_MATCH)
def habitat_match(ent):
    frags = []

    for token in ent:
        frags.append(REPLACE.get(token.lower_, token.lower_))

        if "habitat_term" in token._.data:
            del token._.data["habitat_term"]

    if "habitat_term" in ent._.data:
        del ent._.data["habitat_term"]

    ent._.data["habitat"] = " ".join(frags)


@registry.misc(LABELED_HABITAT_MATCH)
def labeled_habitat_match(ent):
    i = 0
    for i, token in enumerate(ent):
        if token._.term != "habitat_label":
            break
    ent._.data["habitat"] = ent[i:].text
