import re

from spacy import Language

from ... import add_pipe as add
from ... import const
from ... import trait_util
from ... import util
from .elevation_compilers import FLOAT_RE

ELEV_FUNC = "elev_func"

HERE = const.TRAIT_DIR / "elevation"
UNITS = const.TRAIT_DIR / "units"

ELEV_CSV = HERE / "elevation.csv"
UNITS_CSV = UNITS / "units_length.csv"


def pipe(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(
            nlp,
            name="elev_lower",
            attr="lower",
            path=HERE / "elevation_terms_lower.jsonl",
            **kwargs,
        )
        prev = add.term_pipe(
            nlp,
            name="elev_units",
            attr="lower",
            path=UNITS / "units_length_terms_lower.jsonl",
            after=prev,
        )

    prev = add.ruler_pipe(
        nlp,
        name="elev_patterns",
        path=HERE / "elevation_patterns.jsonl",
        after=prev,
        overwrite_ents=True,
    )

    prev = add.data_pipe(nlp, ELEV_FUNC, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name="elev_cleanup",
        remove=trait_util.labels_to_remove([ELEV_CSV, UNITS_CSV], "elevation"),
        after=prev,
    )

    return prev


# ###############################################################################
FACTORS_CM = trait_util.term_data(UNITS_CSV, "factor_cm", float)  # Convert values to cm
FACTORS_M = {k: v / 100.0 for k, v in FACTORS_CM.items()}  # Convert values to meters

UNIT_LABELS = trait_util.get_labels(UNITS_CSV)
UNITS_REPLACE = trait_util.term_data(UNITS_CSV, "replace")


@Language.component(ELEV_FUNC)
def elevation_data(doc):
    for ent in [e for e in doc.ents if e.label_ == "elevation"]:
        values = []
        units = ""
        expected_values = 1

        for token in ent:
            # Find numbers
            if re.match(FLOAT_RE, token.text) and len(values) < expected_values:
                values.append(util.to_positive_float(token.text))

            # Find units
            elif token._.term in UNIT_LABELS and not units:
                units = UNITS_REPLACE.get(token.lower_, token.lower_)

            # If there's a dash it's a range
            elif token.text in const.DASH:
                expected_values = 2

        factor = FACTORS_M[units]
        ent._.data["elevation"] = round(values[0] * factor, 3)
        if expected_values == 2:
            ent._.data["elevation_high"] = round(values[1] * factor, 3)

    return doc
