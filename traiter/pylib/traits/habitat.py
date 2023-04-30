from pathlib import Path

from spacy.language import Language
from spacy.util import registry

from traiter.pylib import add_pipe as add
from traiter.pylib import trait_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes.reject_match import REJECT_MATCH

HABITAT_CSV = Path(__file__).parent / "terms" / "habitat_terms.csv"

REPLACE = trait_util.term_data(HABITAT_CSV, "replace")


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="habitat_terms", path=HABITAT_CSV, **kwargs)

    # prev = add.debug_tokens(nlp, after=prev)  # ##############################

    prev = add.trait_pipe(
        nlp,
        name="habitat_patterns",
        compiler=habitat_compilers(),
        after=prev,
    )

    prev = add.cleanup_pipe(nlp, name="habitat_cleanup", after=prev)

    return prev


def habitat_compilers():
    decoder = {
        "bad": {"ENT_TYPE": "bad_habitat"},
        "habitat": {"ENT_TYPE": "habitat_term"},
        "label": {"ENT_TYPE": "habitat_label"},
        "prefix": {"ENT_TYPE": "habitat_prefix"},
        "sent": {"IS_SENT_START": False},
        "suffix": {"ENT_TYPE": "habitat_suffix"},
    }

    return [
        Compiler(
            label="habitat",
            on_match="habitat_match",
            decoder=decoder,
            keep="habitat",
            patterns=[
                "        habitat+",
                "prefix+ habitat+",
                "prefix+ habitat+ suffix+",
                "        habitat+ suffix+",
                "prefix+          suffix+",
            ],
        ),
        Compiler(
            label="labeled_habitat",
            id="habitat",
            on_match="labeled_habitat_match",
            decoder=decoder,
            keep="habitat",
            patterns=[
                "label+ sent+",
            ],
        ),
        Compiler(
            label="not_habitat",
            decoder=decoder,
            on_match=REJECT_MATCH,
            patterns=[
                "bad habitat+",
                "bad habitat+ bad",
                "    habitat+ bad",
            ],
        ),
    ]


@registry.misc("habitat_match")
def habitat_match(ent):
    frags = []

    for token in ent:
        frags.append(REPLACE.get(token.lower_, token.lower_))

    ent._.data = {"habitat": " ".join(frags)}


@registry.misc("labeled_habitat_match")
def labeled_habitat_match(ent):
    i = 0
    for i, token in enumerate(ent):
        if token._.term != "habitat_label":
            break
    ent._.data = {"habitat": ent[i:].text}
