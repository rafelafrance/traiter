from pathlib import Path

from spacy.language import Language
from spacy.util import registry

from traiter.pylib import add_pipe as add
from traiter.pylib import const
from traiter.pylib import trait_util
from traiter.pylib.pattern_compiler import Compiler

COLOR_CSV = Path(__file__).parent / "terms" / "color_terms.csv"

REPLACE = trait_util.term_data(COLOR_CSV, "replace")
REMOVE = trait_util.term_data(COLOR_CSV, "remove", int)


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="color_terms", path=COLOR_CSV, **kwargs)

    prev = add.trait_pipe(
        nlp,
        name="color_patterns",
        compiler=color_patterns(),
        after=prev,
    )

    prev = add.cleanup_pipe(nlp, name="color_cleanup", after=prev)

    # prev = add.debug_tokens(nlp, after=prev)  # ###########################

    return prev


def color_patterns():
    return [
        Compiler(
            label="color",
            on_match="color_match",
            keep="color",
            decoder={
                "-": {"TEXT": {"IN": const.DASH}},
                "color": {"ENT_TYPE": "color"},
                "color_words": {"ENT_TYPE": {"IN": ["color", "color_mod"]}},
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
