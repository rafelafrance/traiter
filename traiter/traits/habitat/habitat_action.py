from pathlib import Path

from spacy import registry

from traiter.traits import trait_util

HABITAT_MATCH = "habitat_match"

HABITAT_CSV = Path(__file__).parent / "habitat_terms.csv"

REPLACE = trait_util.term_data(HABITAT_CSV, "replace")


@registry.misc(HABITAT_MATCH)
def color_match(ent):
    frags = [REPLACE.get(t.lower_, t.lower_) for t in ent]
    ent._.data["habitat"] = " ".join(frags)
