import re
from pathlib import Path

from spacy import Language

from ... import add_pipe as add
from ... import trait_util
from ... import util
from .lat_long_compilers import FLOAT_RE
from .lat_long_compilers import PUNCT

HERE = Path(__file__).parent
TRAIT = HERE.stem

FUNC = f"{TRAIT}_func"
FUNC_UNCERTAIN = f"{TRAIT}_uncertain_func"

CSV = HERE / f"{TRAIT}.csv"

UNITS = "units_length"
UNITS_DIR = HERE.parent / "units"
UNITS_CSV = UNITS_DIR / f"{UNITS}.csv"


def pipe(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(
            nlp,
            name=f"{TRAIT}_lower",
            attr="lower",
            path=HERE / f"{TRAIT}_terms_lower.jsonl",
            **kwargs,
        )

        prev = add.term_pipe(
            nlp,
            name=f"{TRAIT}_units",
            attr="lower",
            path=UNITS_DIR / f"{UNITS}_terms_lower.jsonl",
            after=prev,
        )

    prev = add.ruler_pipe(
        nlp,
        name=f"{TRAIT}_patterns",
        path=HERE / f"{TRAIT}_patterns.jsonl",
        after=prev,
        overwrite_ents=True,
    )

    prev = add.data_pipe(nlp, FUNC, after=prev)

    prev = add.ruler_pipe(
        nlp,
        name=f"{TRAIT}_uncertain_patterns",
        path=HERE / f"{TRAIT}_uncertain_patterns.jsonl",
        after=prev,
        overwrite_ents=True,
    )

    prev = add.data_pipe(nlp, FUNC_UNCERTAIN, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name=f"{TRAIT}_cleanup",
        remove=trait_util.labels_to_remove([CSV, UNITS_CSV], TRAIT),
        after=prev,
    )

    return prev


# ###############################################################################
FACTORS_CM = trait_util.term_data(UNITS_CSV, "factor_cm", float)  # Convert values to cm
FACTORS_M = {k: v / 100.0 for k, v in FACTORS_CM.items()}  # Convert values to meters

REPLACE = trait_util.term_data(CSV, "replace")


@Language.component(FUNC)
def data_func(doc):
    for ent in [e for e in doc.ents if e.label_ == TRAIT]:
        frags = []
        for token in ent:
            token._.flag = "lat_long"
            if token._.term == "lat_long_label":
                continue
            if token._.term == "datum":
                datum = REPLACE.get(token.lower_, token.text)
                ent._.data["datum"] = datum
            else:
                text = token.text.upper() if len(token.text) == 1 else token.text
                frags.append(text)

        lat_long = " ".join(frags)
        lat_long = re.sub(rf"\s([{PUNCT}])", r"\1", lat_long)
        lat_long = re.sub(rf"(-)\s", r"\1", lat_long)
        ent._.data["lat_long"] = lat_long

        ent[0]._.data = ent._.data  # Save in case there is uncertainty in the lat/long
    return doc


@Language.component(FUNC_UNCERTAIN)
def data_func_uncertain(doc):
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
                units = REPLACE.get(token.lower_, token.lower_)
            elif re.match(FLOAT_RE, token.text):
                value = util.to_positive_float(token.text)
        factor = FACTORS_M[units]
        ent._.data["uncertainty"] = round(value * factor, 3)
    return doc
