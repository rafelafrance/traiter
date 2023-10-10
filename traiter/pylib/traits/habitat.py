from pathlib import Path

from spacy.language import Language
from spacy.util import registry

from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.pipes.reject_match import REJECT_MATCH

from .base import Base

HABITAT_CSV = Path(__file__).parent / "terms" / "habitat_terms.csv"

REPLACE = term_util.term_data(HABITAT_CSV, "replace")

SEP = "/,-"


def build(nlp: Language):
    add.term_pipe(nlp, name="habitat_terms", path=HABITAT_CSV)
    add.trait_pipe(nlp, name="habitat_patterns", compiler=habitat_compilers())
    add.cleanup_pipe(nlp, name="habitat_cleanup")


def habitat_compilers():
    decoder = {
        "bad": {"ENT_TYPE": "bad_habitat"},
        "not_eol": {"LOWER": {"REGEX": r"^[^;.]+$"}},
        "habitat": {"ENT_TYPE": "habitat_term"},
        "label": {"ENT_TYPE": "habitat_label"},
        "prefix": {"ENT_TYPE": "habitat_prefix"},
        "sep": {"LOWER": {"REGEX": rf"[{SEP}]"}},
        "suffix": {"ENT_TYPE": "habitat_suffix"},
    }

    return [
        Compiler(
            label="habitat",
            on_match="habitat_trait",
            decoder=decoder,
            keep="habitat",
            patterns=[
                "        habitat+",
                "prefix+ sep? prefix* habitat+",
                "prefix+ sep? prefix* habitat+ sep? suffix+",
                "        sep? prefix* habitat+ sep? suffix+",
                "prefix+ sep? prefix*          sep? suffix+",
            ],
        ),
        Compiler(
            label="labeled_habitat",
            id="habitat",
            on_match="labeled_habitat",
            decoder=decoder,
            keep="habitat",
            patterns=[
                "label+ not_eol+",
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


class Habitat(Base):
    @classmethod
    def from_ent(cls, ent, **kwargs):
        frags = []

        for token in ent:
            if token.text not in SEP:
                frags.append(REPLACE.get(token.lower_, token.lower_))

        habitat = " ".join(frags)

        return super().from_ent(ent, habitat=habitat)

    @classmethod
    def labeled_match(cls, ent):
        i = 0
        for i, token in enumerate(ent):
            if token._.term != "habitat_label":
                break
        habitat = " ".join(ent[i:].text.split())
        trait = super().from_ent(ent, habitat=habitat)
        trait.trait = "habitat"
        return trait


@registry.misc("habitat_trait")
def habitat_trait(ent):
    return Habitat.from_ent(ent)


@registry.misc("labeled_habitat")
def labeled_habitat(ent):
    return Habitat.labeled_match(ent)
