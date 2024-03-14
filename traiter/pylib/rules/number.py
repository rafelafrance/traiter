import re
from dataclasses import dataclass

from spacy import Language, registry

from traiter.pylib import const as t_const
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules.base import Base
from traiter.pylib.util import to_positive_float as as_float

FLOAT_RE: str = r"\d{1,4}(\.\d{,3})?"
FLOAT3_RE: str = r"\d{3}(\.\d{,3})?"
INT_RE: str = r"\d{1,4}"
DEC_RE: str = r"\.\d{1,3}"

FACT_LEN = 2

# This pipe is used multiple times
NUMBER_COUNT = 0  # Used to rename the Number pipe


@dataclass(eq=False)
class Number(Base):
    number: float = None
    is_fraction: bool = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn()

    @classmethod
    def pipe(cls, nlp: Language, _overwrite: list[str] | None = None):
        global NUMBER_COUNT
        NUMBER_COUNT += 1
        add.trait_pipe(
            nlp, name=f"fraction_{NUMBER_COUNT}", compiler=cls.fraction_patterns()
        )
        # add.debug_tokens(nlp)  # ###########################################

        add.trait_pipe(
            nlp, name=f"number_{NUMBER_COUNT}", compiler=cls.number_patterns()
        )
        # add.debug_tokens(nlp)  # ###########################################

    @classmethod
    def number_patterns(cls):
        decoder = {
            ",": {"TEXT": {"IN": t_const.COMMA}},
            "99.0": {"LOWER": {"REGEX": f"^{FLOAT_RE}+$"}},
            "999.0": {"LOWER": {"REGEX": f"^{FLOAT3_RE}+$"}},
            "99": {"LOWER": {"REGEX": f"^{INT_RE}+$"}},
            ".99": {"LOWER": {"REGEX": f"^{DEC_RE}+$"}},
        }
        return [
            Compiler(
                label="number",
                keep="number",
                on_match="number_match",
                decoder=decoder,
                patterns=[
                    " 99.0 ",
                    " 99 , 999.0 ",
                    " .99 ",
                ],
            ),
        ]

    @classmethod
    def fraction_patterns(cls):
        decoder = {
            "/": {"TEXT": {"IN": t_const.SLASH}},
            "99": {"LOWER": {"REGEX": f"^{INT_RE}+$"}},
        }
        return [
            Compiler(
                label="number",
                keep="number",
                on_match="fract_match",
                decoder=decoder,
                patterns=[
                    "    99 / 99 ",
                    " 99 99 / 99 ",
                ],
            ),
        ]

    @classmethod
    def number_match(cls, ent):
        number = as_float(ent.text)
        trait = cls.from_ent(ent, number=number)
        ent[0]._.trait = trait
        ent[0]._.flag = "number"
        return trait

    @classmethod
    def fract_match(cls, ent):
        numbers = [as_float(t.text) for t in ent if re.match(INT_RE, t.text)]

        number = numbers[-2] / numbers[-1]  # Calculate the fraction part
        # Add in the whole number part
        number += numbers[0] if len(numbers) > FACT_LEN else 0.0

        trait = cls.from_ent(ent, number=number, is_fraction=True)

        ent[0]._.trait = trait
        ent[0]._.flag = "number"

        return trait


@registry.misc("number_match")
def number_match(ent):
    return Number.number_match(ent)


@registry.misc("fract_match")
def fract_match(ent):
    return Number.fract_match(ent)
