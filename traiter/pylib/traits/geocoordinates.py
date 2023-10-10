import re
from pathlib import Path

from spacy.language import Language
from spacy.util import registry

from traiter.pylib import const, term_util, util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add, reject_match

from .base import Base

SYM = r"""°"”“'`‘´’"""
PUNCT = f"""{SYM},;._"""

FLOAT_RE = r"\d+(\.\d+)?"
FLOAT_LL = r"\d{1,3}(\.\d+)?"

PLUS = r"^(±|\+|-|\+-|-\+)+\Z"
MINUS = r"^[-]\Z"

GEOCOORDINATES_CSV = Path(__file__).parent / "terms" / "geocoordinate_terms.csv"
UNIT_CSV = Path(__file__).parent / "terms" / "unit_length_terms.csv"
ALL_CSVS = [GEOCOORDINATES_CSV, UNIT_CSV]

REPLACE = term_util.term_data([UNIT_CSV, GEOCOORDINATES_CSV], "replace")
FACTORS_CM = term_util.term_data(UNIT_CSV, "factor_cm", float)
FACTORS_M = {k: v / 100.0 for k, v in FACTORS_CM.items()}

DIR = """((north|east|south|west)(ing)?|[nesw])"""


def build(nlp: Language):
    add.term_pipe(nlp, name="geocoordinate_terms", path=ALL_CSVS)
    add.trait_pipe(
        nlp, name="geocoordinate_patterns", compiler=geocoordinate_patterns()
    )
    add.trait_pipe(
        nlp,
        name="geocoordinate_plus_patterns",
        overwrite=["lat_long"],
        compiler=geocoordinate_plus_patterns(),
    )
    add.cleanup_pipe(nlp, name="geocoordinate_cleanup")


def geocoordinate_patterns():
    decoder = {
        "(": {"TEXT": {"IN": const.OPEN}},
        ")": {"TEXT": {"IN": const.CLOSE}},
        "+99.0": {"TEXT": {"REGEX": r"^(±|\+|-)?\d{1,3}(\.\d+)?\Z"}},
        ",": {"TEXT": {"REGEX": r"^[,;._:]\Z"}},
        "/": {"TEXT": {"IN": const.SLASH}},
        "-": {"TEXT": {"IN": const.DASH}},
        "'s": {"LOWER": "'s"},
        "99": {"LOWER": {"REGEX": r"^\d{1,2}$"}},
        "9999": {"LOWER": {"REGEX": r"^\d+$"}},
        "99.0": {"TEXT": {"REGEX": rf"^{FLOAT_LL}$"}},
        "99.99": {"TEXT": {"REGEX": r"^\d+\.\d{2,}$"}},
        "[+]": {"TEXT": {"REGEX": PLUS}},
        "[-]": {"TEXT": {"REGEX": PLUS}},
        "datum": {"ENT_TYPE": "datum"},
        "datum_label": {"ENT_TYPE": "datum_label"},
        "deg": {"LOWER": {"REGEX": rf"""^([{SYM}]|degrees?|deg\.?|d)\Z"""}},
        "dir": {"LOWER": {"REGEX": r"""^'?[nesw]\.?\Z"""}},
        "dir99.0": {"LOWER": {"REGEX": rf"""^[nesw]{FLOAT_LL}\Z"""}},
        "key": {"ENT_TYPE": "lat_long_key"},
        "label": {"ENT_TYPE": "lat_long_label"},
        "m": {"ENT_TYPE": {"IN": ["metric_length", "imperial_length"]}},
        "min": {"LOWER": {"REGEX": rf"""^([{SYM}]|minutes?|min\.?|m)\Z"""}},
        "sec": {"LOWER": {"REGEX": rf"""^([{SYM}]|seconds?|sec\.?|s)\Z"""}},
        "sect": {"LOWER": {"REGEX": r"""^(section|sec\.?|s)$"""}},
        "sp": {"IS_SPACE": True},
        "trs_post": {"LOWER": {"REGEX": r"^[nesw]$"}},
        "trs_pre": {"LOWER": {"REGEX": r"^[neswrst]{1,2}\d*$"}},
        "uaa": {"LOWER": {"REGEX": r"^u[a-z]{1,2}$"}},
        "uncert": {"ENT_TYPE": "uncertain_label"},
        "utm_dir": {"LOWER": {"REGEX": rf"""^{DIR}\Z"""}},
        "utm_label": {"ENT_TYPE": "utm_label"},
    }

    return [
        Compiler(
            label="lat_long",
            on_match="lat_long_trait",
            keep="lat_long",
            decoder=decoder,
            patterns=[
                (
                    "label* sp? [-]? 99.0 deg 99.0? min* 99.0? sec* ,* sp? "
                    "           [-]? 99.0 deg 99.0? min* 99.0? sec* (? datum* )?"
                ),
                (
                    "label* sp? [-]? 99.0 deg* 99.0? min* 99.0? sec* dir  ,* sp? "
                    "           [-]? 99.0 deg* 99.0? min* 99.0? sec* dir  (? datum* )?"
                ),
                (
                    "label* sp? dir [-]? 99.0 deg* 99.0? min* 99.0? sec* ,* sp? "
                    "           dir [-]? 99.0 deg* 99.0? min* 99.0? sec* (? datum* )?"
                ),
                (
                    "key ,* [-]? 99.0 deg* 99.0? min* 99.0? sec* dir? ,* sp? "
                    "key ,* [-]? 99.0 deg* 99.0? min* 99.0? sec* dir? (? datum* )?"
                ),
                (
                    "[-]? 99.0 deg* 99.0? min* 99.0? sec* dir? key ,* sp? "
                    "[-]? 99.0 deg* 99.0? min* 99.0? sec* dir? key ,* (? datum* )?"
                ),
                (
                    "key ,* [-]? 99.0 deg* 99.0? min* 99.0? sec* dir? [-] sp? "
                    "99.0 deg* 99.0? min* 99.0? sec* dir? ,*  sp? "
                    "key ,* [-]? 99.0 deg* 99.0? min* 99.0? sec* dir? [-] sp? "
                    "99.0 deg* 99.0? min* 99.0? sec* dir? (? datum* )?"
                ),
                (
                    "label* sp? dir99.0 deg* 99.0? min* 99.0? sec* ,* sp? "
                    "           dir99.0 deg* 99.0? min* 99.0? sec* (? datum* )?"
                ),
                (
                    "label* sp? [-]? 99.0 deg 99.0? min* -? 99.0? sec* dir? ,* sp? "
                    "          [-]? 99.0 deg 99.0? min* -? 99.0? sec* dir? (? datum* )?"
                ),
                (
                    "label* sp? [-]? 99.0 deg 99.0? min* -? 99.0? 's ,* sp? "
                    "          [-]? 99.0 deg 99.0? min* -? 99.0? sec* dir? (? datum* )?"
                ),
                "label* sp? [-]? 99.99 dir? ,* sp? [-]? 99.99 dir? (? datum* )?",
            ],
        ),
        Compiler(
            label="trs_part",
            keep="trs",
            decoder=decoder,
            on_match="trs_part",
            patterns=[
                " trs_pre         ,?",
                " trs_pre /? 99   ,?",
                " trs_pre /? trs_post ,? ",
            ],
        ),
        Compiler(
            label="utm",
            keep="utm",
            decoder=decoder,
            on_match="utm_trait",
            patterns=[
                "utm_label* 99 sect ,* 9999 utm_dir? ,* 9999 utm_dir? (? datum* )?",
                "99 uaa 9999",
            ],
        ),
    ]


def geocoordinate_plus_patterns():
    decoder = {
        "-": {"TEXT": {"IN": const.DASH}},
        ",": {"TEXT": {"REGEX": r"^[,;._:]\Z"}},
        "(": {"TEXT": {"IN": const.OPEN}},
        ")": {"TEXT": {"IN": const.CLOSE}},
        "datum": {"ENT_TYPE": "datum"},
        "datum_label": {"ENT_TYPE": "datum_label"},
        "m": {"ENT_TYPE": {"IN": ["metric_length", "imperial_length"]}},
        "99.0": {"TEXT": {"REGEX": rf"^{FLOAT_RE}$"}},
        "+99.0": {"TEXT": {"REGEX": r"^(±|\+|-)?\d+(\.\d+)?\Z"}},
        "uncert": {"ENT_TYPE": "uncertain_label"},
        "lat_long": {"ENT_TYPE": "lat_long"},
        "[+]": {"TEXT": {"REGEX": PLUS}},
        "99": {"IS_DIGIT": True},
        "sec_label": {"ENT_TYPE": "sec_label"},
        "trs_label": {"ENT_TYPE": "trs_label"},
        "trs": {"ENT_TYPE": "trs_part"},
        "not_trs": {"ENT_TYPE": "not_trs"},
    }
    return [
        Compiler(
            label="lat_long_uncertain",
            id="lat_long",
            on_match="lat_long_uncertain",
            keep=["lat_long"],
            decoder=decoder,
            patterns=[
                "lat_long+                              datum_label+ ,* (? datum+ )?",
                "lat_long+ ,? uncert? ,?     +99.0 m ,* datum_label* ,* (? datum* )?",
                "lat_long+ ,? uncert? ,? [+]* 99.0 m ,* datum_label* ,* (? datum* )?",
                (
                    "lat_long+ ,? uncert? ,? [+]* 99.0 - 99.0 m ,* "
                    "datum_label* ,* (? datum* )?"
                ),
            ],
        ),
        Compiler(
            label="trs",
            keep="trs",
            on_match="trs_trait",
            decoder=decoder,
            patterns=[
                " trs_label* trs+",
                " trs_label* trs+ sec_label+ 99",
                " trs_label* trs+ sec_label+ 99 ,? 99",
                " trs_label* sec_label+ 99 ,? trs+",
            ],
        ),
        Compiler(
            label="not_trs",
            on_match=reject_match.REJECT_MATCH,
            decoder=decoder,
            patterns=[
                "        trs+ not_trs",
                "not_trs trs+ not_trs",
                "not_trs trs+",
            ],
        ),
    ]


def format_coords(frags):
    coords = " ".join(frags)
    coords = re.sub(rf"\s([{PUNCT}])", r"\1", coords)
    coords = re.sub(r"\s(:)", r"\1", coords)
    coords = re.sub(r"(?<=\d)([NESWnesw])", r" \1", coords)
    coords = re.sub(r"-\s(?=\d)", r"-", coords)
    coords = " ".join(coords.split())
    return coords


class LatLong(Base):
    @classmethod
    def from_ent(cls, ent, **kwargs):
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

        lat_long = format_coords(frags)

        if datum:
            datum = "".join(datum)
            datum = REPLACE.get(datum, datum)
        else:
            datum = None

        ent[0]._.flag = "lat_long_data"

        trait = super().from_ent(ent, lat_long=lat_long, datum=datum)
        ent[0]._.trait = trait  # Save for uncertainty in the lat/long
        return trait

    @classmethod
    def lat_long_uncertain(cls, ent):
        value = 0.0
        unit = []
        datum = []
        kwargs = {}

        for token in ent:
            # Get the data from the original parse
            if token._.flag == "lat_long_data":
                kwargs = token._.trait.as_dict()
                for key in ("trait", "start", "end"):
                    del kwargs[key]

            # Get the uncertainty units
            elif token._.term in ("metric_length", "imperial_length"):
                unit.append(token.lower_)

            # Already parsed
            elif token._.flag:
                continue

            # Pick up a trailing datum
            elif token._.term == "datum":
                datum.append(token.lower_)

            # Get the uncertainty value
            elif re.match(const.FLOAT_RE, token.text):
                value = util.to_positive_float(token.text)

        if value and not unit:
            raise reject_match.RejectMatch

        # Convert the values to meters
        if value:
            unit = "".join(unit)
            unit = REPLACE.get(unit, unit)
            kwargs["units"] = "m"
            factor = FACTORS_M[unit]
            kwargs["uncertainty"] = round(value * factor, 3)
        else:
            kwargs["units"] = None
            kwargs["uncertainty"] = None

        datum = "".join(datum)
        kwargs["datum"] = REPLACE.get(datum, datum) if datum else None

        trait = super().from_ent(ent, **kwargs)
        trait.trait = "lat_long"
        return trait


class TRS(Base):
    @classmethod
    def trs_part(cls, ent):
        # Enforce a minimum length
        if len(ent.text) < 3:
            raise reject_match.RejectMatch

        trait = super().from_ent(ent, trs_part=ent.text)

        for token in ent:
            token._.flag = "trs_part"

        ent[0]._.trait = trait
        ent[0]._.flag = "trs_data"

        return trait

    @classmethod
    def from_ent(cls, ent, **kwargs):
        frags = []

        for token in ent:
            if token._.flag == "trs_data":
                frags.append(token._.trait.trs_part)

            elif token._.flag == "trs_part":
                continue

            elif re.match(r"^(\d+|,)$", token.text):
                frags.append(token.text)

            elif token._.term == "sec_label":
                frags.append(token.lower_)

        trs = " ".join(frags)
        trs = re.sub(r"\s([.,:])", r"\1", trs)
        trs = re.sub(r",$", "", trs)
        if len(trs.split()) < 2:
            raise reject_match.RejectMatch

        return super().from_ent(ent, trs="present")


class UTM(Base):
    @classmethod
    def from_ent(cls, ent, **kwargs):
        frags = []
        datum = []

        for token in ent:
            if token._.term == "utm_label":
                continue

            if token.text in const.OPEN + const.CLOSE:
                continue

            if token._.term == "datum":
                datum.append(token.lower_)

            else:
                text = token.text.upper() if len(token.text) == 1 else token.text
                frags.append(text)

        if datum:
            datum = "".join(datum)
            datum = REPLACE.get(datum, datum)
        else:
            datum = None

        return super().from_ent(ent, utm=format_coords(frags), datum=datum)


@registry.misc("lat_long_trait")
def lat_long_trait(ent):
    return LatLong.from_ent(ent)


@registry.misc("lat_long_uncertain")
def lat_long_uncertain(ent):
    return LatLong.lat_long_uncertain(ent)


@registry.misc("trs_part")
def trs_part(ent):
    return TRS.trs_part(ent)


@registry.misc("trs_trait")
def trs_trait(ent):
    return TRS.from_ent(ent)


@registry.misc("utm_trait")
def utm_trait(ent):
    return UTM.from_ent(ent)
