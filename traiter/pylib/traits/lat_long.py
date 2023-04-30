import re
from pathlib import Path

from spacy.language import Language
from spacy.util import registry

from traiter.pylib import add_pipe as add
from traiter.pylib import const
from traiter.pylib import trait_util
from traiter.pylib import util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes.reject_match import RejectMatch

SYM = r"""°"”“'`‘´’"""
PUNCT = f"""{SYM},;._"""

_180 = r"[-]?(1\d\d|\d\d?)([.,_;]\d+)?"
_90 = r"[-]?([1-9]\d|\d)([.,_;]\d+)?"
_60 = r"[-]?([1-6]\d|\d)([.,_;]\d+)?"

FLOAT_RE = r"^([\d,]+\.?\d*)\Z"
NUM_PLUS = r"^(±|\+|-)?[\d,]+\.?\d*\Z"
PLUS = r"^(±|\+|-)+\Z"
MINUS = r"^[-]\Z"

LAT_LONG_CSV = Path(__file__).parent / "terms" / "lat_long_terms.csv"
UNIT_CSV = Path(__file__).parent / "terms" / "unit_length_terms.csv"
ALL_CSVS = [LAT_LONG_CSV, UNIT_CSV]

REPLACE = trait_util.term_data([UNIT_CSV, LAT_LONG_CSV], "replace")
FACTORS_CM = trait_util.term_data(UNIT_CSV, "factor_cm", float)
FACTORS_M = {k: v / 100.0 for k, v in FACTORS_CM.items()}


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="lat_long_terms", path=ALL_CSVS, **kwargs)

    prev = add.trait_pipe(
        nlp,
        name="lat_long_patterns",
        compiler=lat_long_compilers(),
        after=prev,
    )

    # prev = add.debug_tokens(nlp, after=prev)  # ##################################

    prev = add.trait_pipe(
        nlp,
        name="lat_long_uncertain_patterns",
        compiler=lat_long_uncertain_compilers(),
        after=prev,
    )

    prev = add.cleanup_pipe(nlp, name="lat_long_cleanup", after=prev)

    return prev


def decoder():
    return {
        ",": {"TEXT": {"REGEX": r"^[,;._:]\Z"}},
        "(": {"TEXT": {"IN": const.OPEN}},
        ")": {"TEXT": {"IN": const.CLOSE}},
        "key": {"ENT_TYPE": "lat_long_key"},
        "label": {"ENT_TYPE": "lat_long_label"},
        "deg": {"LOWER": {"REGEX": rf"""^([{SYM}]|degrees?|deg\.?)\Z"""}},
        "min": {"LOWER": {"REGEX": rf"""^([{SYM}]|minutes?|min\.?)\Z"""}},
        "sec": {"LOWER": {"REGEX": rf"""^([{SYM}]|seconds?|sec\.?)\Z"""}},
        "dir": {"LOWER": {"REGEX": r"""^[nesw]\.?\Z"""}},
        "180": {"TEXT": {"REGEX": rf"""^{_180}\Z"""}},
        "90": {"TEXT": {"REGEX": rf"""^{_90}\Z"""}},
        "60": {"TEXT": {"REGEX": rf"""^{_60}\Z"""}},
        "datum": {"ENT_TYPE": "datum"},
        "m": {"ENT_TYPE": {"IN": ["metric_length", "imperial_length"]}},
        "99": {"TEXT": {"REGEX": FLOAT_RE}},
        "+99": {"TEXT": {"REGEX": NUM_PLUS}},
        "uncert": {"ENT_TYPE": "uncertain_label"},
        "lat_long": {"ENT_TYPE": "lat_long"},
        "[+]": {"TEXT": {"REGEX": PLUS}},
        "[-]": {"TEXT": {"REGEX": PLUS}},
    }


def lat_long_compilers():
    return Compiler(
        label="lat_long",
        on_match="lat_long_match",
        keep="lat_long",
        decoder=decoder(),
        patterns=[
            "label? [-]? 180 deg*                 dir ,* [-]? 180 deg*                 dir datum*",
            "label? [-]? 180 deg* 60 min*         dir ,* [-]? 180 deg* 60 min*         dir datum*",
            "label? [-]? 180 deg* 60 min* 60 sec* dir ,* [-]? 180 deg* 60 min* 60 sec* dir datum*",
            "label? dir [-]? 180 deg*                 ,* dir [-]? 180 deg*                 datum*",
            "label? dir [-]? 180 deg* 60 min* 60 sec* ,* dir [-]? 180 deg* 60 min* 60 sec* datum*",
            "label? dir [-]? 180 deg* 60 min*         ,* dir [-]? 180 deg* 60 min*         datum*",
            "key ,* [-]? 90                           ,* key ,* [-]? 90",
            "key ,* [-]? 90                           ,* key ,* [-]? 90 ( datum+ )",
            "key ,* [-]? 90                           ,* key ,* [-]? 90   datum+",
            "key ,* [-]? 180 deg*                 dir ,* key ,* [-]? 180 deg*                 dir datum*",
            "key ,* [-]? 180 deg* 60 min*         dir ,* key ,* [-]? 180 deg* 60 min*         dir datum*",
            "key ,* [-]? 180 deg* 60 min* 60 sec* dir ,* key ,* [-]? 180 deg* 60 min* 60 sec* dir datum*",
        ],
    )


def lat_long_uncertain_compilers():
    return Compiler(
        label="lat_long_uncertain",
        id="lat_long",
        on_match="lat_long_uncertain_match",
        keep=["lat_long"],
        decoder=decoder(),
        patterns=[
            "lat_long+ ,? uncert? ,?     +99 m",
            "lat_long+ ,? uncert? ,? [+]? 99 m",
        ],
    )


@registry.misc("lat_long_match")
def lat_long_match(ent):
    frags = []
    datum = []
    for token in ent:
        token._.flag = "lat_long"

        if token._.term == "lat_long_label":
            continue

        if token.text in const.OPEN + const.CLOSE:
            continue

        if token._.term == "datum":
            datum.append(token.lower_)

        else:
            text = token.text.upper() if len(token.text) == 1 else token.text
            frags.append(text)

    lat_long = " ".join(frags)
    lat_long = re.sub(rf"\s([{PUNCT}])", r"\1", lat_long)
    lat_long = re.sub(r"(-)\s", r"\1", lat_long)
    lat_long = re.sub(r"\s(:)", r"\1", lat_long)
    lat_long = re.sub(r"(?<=\d)([NESWnesw])", r" \1", lat_long)

    ent._.data = {"lat_long": lat_long}

    if datum:
        datum = "".join(datum)
        ent._.data["datum"] = REPLACE.get(datum, datum)

    ent[0]._.data = ent._.data  # Save for uncertainty in the lat/long
    ent[0]._.flag = "lat_long_data"


@registry.misc("lat_long_uncertain_match")
def lat_long_uncertain_match(ent):
    unit = ""
    value = 0.0
    for token in ent:
        # Get the data from the original parse
        if token._.flag == "lat_long_data":
            ent._.data = token._.data

        # Get the uncertainty units
        elif token._.term in ("metric_length", "imperial_length"):
            unit = REPLACE.get(token.lower_, token.lower_)

        # Already parse
        elif token._.flag:
            continue

        # Get the uncertainty value
        elif re.match(const.FLOAT_RE, token.text):
            value = util.to_positive_float(token.text)

    if not unit:
        raise RejectMatch

    # Convert the values to meters
    ent._.data["units"] = "m"
    factor = FACTORS_M[unit]
    ent._.data["uncertainty"] = round(value * factor, 3)
