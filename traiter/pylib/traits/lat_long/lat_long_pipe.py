import re

from spacy import Language

from .. import add
from .. import trait_util
from ... import const
from ... import util
from .lat_long_compilers import FLOAT_RE
from .lat_long_compilers import PUNCT

# from ...pipes import debug

LAT_LONG_FUNC = "lat_long_func"
LAT_LONG_UNCERTAIN_FUNC = "lat_long_uncertain_func"

HERE = const.TRAIT_DIR / "lat_long"
UNITS_DIR = const.TRAIT_DIR / "units"
UNITS_CSV = UNITS_DIR / "units_length.csv"

LAT_LONG_CSV = HERE / "lat_long.csv"


def pipe(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(
            nlp,
            name="lat_long_lower",
            attr="lower",
            path=HERE / "lat_long_terms_lower.jsonl",
            **kwargs,
        )

        prev = add.term_pipe(
            nlp,
            name="lat_long_units",
            attr="lower",
            path=UNITS_DIR / "units_length_terms_lower.jsonl",
            after=prev,
        )

    prev = add.ruler_pipe(
        nlp,
        name="lat_long_patterns",
        path=HERE / "lat_long_patterns.jsonl",
        after=prev,
        overwrite_ents=True,
    )

    prev = add.data_pipe(nlp, LAT_LONG_FUNC, after=prev)

    prev = add.ruler_pipe(
        nlp,
        name="lat_long_uncertain_patterns",
        path=HERE / "lat_long_uncertain_patterns.jsonl",
        after=prev,
        overwrite_ents=True,
    )

    prev = add.data_pipe(nlp, LAT_LONG_UNCERTAIN_FUNC, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name="lat_long_cleanup",
        remove=trait_util.labels_to_remove([LAT_LONG_CSV, UNITS_CSV], "lat_long"),
        after=prev,
    )

    return prev


# ###############################################################################
FACTORS_CM = trait_util.term_data(UNITS_CSV, "factor_cm", float)  # Convert values to cm
FACTORS_M = {k: v / 100.0 for k, v in FACTORS_CM.items()}  # Convert values to km

LAT_LONG_REPLACE = trait_util.term_data(LAT_LONG_CSV, "replace")


@Language.component(LAT_LONG_FUNC)
def lat_long_data(doc):
    for ent in [e for e in doc.ents if e.label_ == "lat_long"]:
        parts = []
        for token in ent:
            token._.flag = "lat_long"
            if token._.term == "lat_long_label":
                continue
            if token._.term == "datum":
                datum = LAT_LONG_REPLACE.get(token.lower_, token.text)
                ent._.data["datum"] = datum
            else:
                text = token.text.upper() if len(token.text) == 1 else token.text
                parts.append(text)

        lat_long = " ".join(parts)
        lat_long = re.sub(rf"\s([{PUNCT}])", r"\1", lat_long)
        lat_long = re.sub(rf"(-)\s", r"\1", lat_long)
        ent._.data["lat_long"] = lat_long

        ent[0]._.data = ent._.data  # Save in case there is uncertainty in the lat/long
    return doc


@Language.component(LAT_LONG_UNCERTAIN_FUNC)
def on_lat_long_uncertain_match(doc):
    for ent in doc.ents:
        if ent.label_ != "lat_long" or ent.id_ != "lat_long_uncertain":
            continue
        units = ""
        value = 0.0
        for token in ent:
            if token._.data:
                ent._.data = token._.data
            elif token._.flag:
                continue
            elif token._.term in ["metric_length", "imperial_length"]:
                units = LAT_LONG_REPLACE.get(token.lower_, token.lower_)
            elif re.match(FLOAT_RE, token.text):
                value = util.to_positive_float(token.text)
        factor = FACTORS_M[units]
        ent._.data["uncertainty"] = round(value * factor, 3)
    return doc
