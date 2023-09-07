from pathlib import Path

from spacy.language import Language
from spacy.util import registry

from traiter.pylib import const, term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

COLOR_CSV = Path(__file__).parent / "terms" / "color_terms.csv"

REPLACE = term_util.term_data(COLOR_CSV, "replace")
REMOVE = term_util.term_data(COLOR_CSV, "remove", int)


def build(nlp: Language):
    add.term_pipe(nlp, name="color_terms", path=COLOR_CSV)
    # add.debug_tokens(nlp)  # ##############################################
    add.trait_pipe(nlp, name="color_patterns", compiler=color_patterns())
    # add.debug_tokens(nlp)  # ##############################################
    add.cleanup_pipe(nlp, name="color_cleanup")


def color_patterns():
    return [
        Compiler(
            label="color",
            on_match="color_match",
            keep="color",
            decoder={
                "-": {"TEXT": {"IN": const.DASH}},
                "color": {"ENT_TYPE": "color_term"},
                "color_words": {"ENT_TYPE": {"IN": ["color_term", "color_mod"]}},
                "missing": {"ENT_TYPE": "color_missing"},
                "to": {"POS": {"IN": ["AUX"]}},
            },
            patterns=[
                "missing? color_words* -* color+ -* color_words*",
                "missing? color_words+ to color_words+ color+ -* color_words*",
            ],
        ),
    ]


@registry.misc("color_match")
def color_match(ent):
    frags = []
    missing = False

    for token in ent:
        # Skip anything that is not a term or is flagged for removal
        if not token._.term or REMOVE.get(token.lower_) or token.text in const.DASH:
            continue

        # Color is noted as missing
        if token._.term == "color_missing":
            missing = True
            continue

        frag = REPLACE.get(token.lower_, token.lower_)

        # Skip duplicate colors within the entity
        if frag not in frags:
            frags.append(frag)

    # Build the color
    value = "-".join(frags)
    ent._.data = {
        "color": REPLACE.get(value, value),
    }
    if missing:
        ent._.data["missing"] = True
