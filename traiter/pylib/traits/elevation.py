import re
from pathlib import Path

from spacy.language import Language
from spacy.util import registry

from traiter.pylib import const, term_util, util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from .base import Base


class Elevation(Base):
    float_re = r"^(\d[\d,.]+)\Z"
    units = ["metric_length", "imperial_length"]

    elevation_csv = Path(__file__).parent / "terms" / "elevation_terms.csv"
    unit_csv = Path(__file__).parent / "terms" / "unit_length_terms.csv"
    about_csv = Path(__file__).parent / "terms" / "about_terms.csv"
    all_csvs = [elevation_csv, unit_csv, about_csv]

    replace = term_util.term_data([unit_csv, elevation_csv], "replace")
    factors_cm = term_util.term_data(unit_csv, "factor_cm", float)
    factors_m = {k: v / 100.0 for k, v in factors_cm.items()}

    def __init__(
        self,
        trait: str = None,
        start: int = None,
        end: int = None,
        elevation: float = None,
        elevation_high: float = None,
        units: str = None,
        about: bool = None,
    ):
        super().__init__(trait, start, end)
        self.elevation = elevation
        self.elevation_high = elevation_high
        self.units = units
        self.about = about

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="elevation_terms", path=cls.all_csvs)
        add.trait_pipe(
            nlp, name="elevation_patterns", compiler=cls.elevation_compilers()
        )
        add.cleanup_pipe(nlp, name="elevation_cleanup")

    @classmethod
    def elevation_compilers(cls):
        label_ender = r"[:=;,.]"
        return [
            Compiler(
                label="elevation",
                on_match="elevation_match",
                keep="elevation",
                decoder={
                    "(": {"TEXT": {"IN": const.OPEN}},
                    ")": {"TEXT": {"IN": const.CLOSE}},
                    "-/to": {"LOWER": {"IN": [*const.DASH, "to", "_"]}, "OP": "+"},
                    "/": {"TEXT": {"IN": const.SLASH}},
                    "99": {"TEXT": {"REGEX": cls.float_re}},
                    ":": {"TEXT": {"REGEX": rf"^{label_ender}+\Z"}},
                    ",": {"TEXT": {"REGEX": rf"^{label_ender}+\Z"}},
                    "about": {"ENT_TYPE": "about"},
                    "label": {"ENT_TYPE": "elev_label"},
                    "m": {"ENT_TYPE": {"IN": cls.units}},
                    "sp": {"IS_SPACE": True},
                },
                patterns=[
                    "label+ :? sp? about? ,? 99 m",
                    "label+ :? sp? about? ,? 99 m ( 99 m ,? )",
                    "label+ :? sp? about? ,? 99 m / 99 m",
                    "              about? ,? 99 m ( 99 m ,? )",
                    "              about? ,? 99 m / 99 m",
                    "label+ :? sp? about? ,? 99 -/to 99 m",
                ],
            ),
        ]

    @classmethod
    def elevation_match(cls, ent):
        values = []
        units_ = ""
        expected_len = 1
        about = None
        hi = None

        for token in ent:
            # Find numbers
            if re.match(const.FLOAT_RE, token.text) and len(values) < expected_len:
                values.append(util.to_positive_float(token.text))

            # Find units
            elif token._.term in cls.units and not units_:
                units_ = cls.replace.get(token.lower_, token.lower_)

            elif token._.term == "about":
                about = True

            # If there's a dash it's a range
            elif token.lower_ in [*const.DASH, "to", "_"]:
                expected_len = 2

        factor = cls.factors_m[units_]

        elevation = round(values[0] * factor, 3)
        units = "m"

        # Handle an elevation range
        if expected_len == 2:
            hi = round(values[1] * factor, 3)

        return super().from_ent(
            ent, elevation=elevation, elevation_high=hi, units=units, about=about
        )


@registry.misc("elevation_match")
def elevation_match(ent):
    return Elevation.elevation_match(ent)
