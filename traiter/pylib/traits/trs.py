import re
from pathlib import Path

from spacy.language import Language
from spacy.util import registry

from traiter.pylib import const
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add, reject_match

TRS_CSV = Path(__file__).parent / "terms" / "trs_terms.csv"


def build(nlp: Language):
    add.term_pipe(nlp, name="trs_terms", path=TRS_CSV)
    add.trait_pipe(nlp, name="trs_part_patterns", compiler=trs_part_patterns())
    add.trait_pipe(nlp, name="trs_patterns", compiler=trs_patterns())
    # add.debug_tokens(nlp)  # ########################################
    add.cleanup_pipe(nlp, name="trs_cleanup")


def trs_part_patterns():
    decoder = {
        ",": {"TEXT": {"IN": const.COMMA}},
        "/": {"TEXT": {"IN": const.SLASH}},
        "99": {"LOWER": {"REGEX": r"^\d{1,2}$"}},
        "post": {"LOWER": {"REGEX": r"^[nesw]$"}},
        "pre": {"LOWER": {"REGEX": r"^[neswrst]{1,2}\d*$"}},
    }

    return Compiler(
        label="trs_part",
        decoder=decoder,
        on_match="trs_part",
        patterns=[
            " pre         ,?",
            " pre /? 99   ,?",
            " pre /? post ,? ",
        ],
    )


def trs_patterns():
    decoder = {
        ",": {"TEXT": {"IN": const.COMMA}},
        "99": {"IS_DIGIT": True},
        "sec_label": {"ENT_TYPE": "sec_label"},
        "trs_label": {"ENT_TYPE": "trs_label"},
        "trs": {"ENT_TYPE": "trs_part"},
    }

    return Compiler(
        label="trs",
        keep="trs",
        on_match="trs",
        decoder=decoder,
        patterns=[
            " trs_label* trs+",
            " trs_label* trs+ sec_label 99",
            " trs_label* trs+ sec_label 99 ,? 99",
            " trs_label* sec_label 99 ,? trs+",
        ],
    )


@registry.misc("trs_part")
def trs_part(ent):
    # Enforce a minimum length
    if len(ent.text) < 3:
        raise reject_match.RejectMatch

    ent._.data["trs_part"] = ent.text

    for token in ent:
        token._.flag = "trs_part"

    ent[0]._.data = ent._.data
    ent[0]._.flag = "trs_data"


@registry.misc("trs")
def trs(ent):
    frags = []

    for token in ent:
        if token._.flag == "trs_data":
            frags.append(token._.data["trs_part"])

        elif token._.flag == "trs_part":
            continue

        elif re.match(r"^(\d+|,)$", token.text):
            frags.append(token.text)

        elif token.ent_type_ == "sec_label":
            frags.append(token.lower_)

    frags = " ".join(frags)
    frags = re.sub(r"\s([,:])", r"\1", frags)
    frags = re.sub(r",$", "", frags)
    ent._.data = {"trs": frags}
