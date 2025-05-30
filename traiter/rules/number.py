import re
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry

from traiter.pipes.reject_match import RejectMatch
from traiter.pylib import add, term_util
from traiter.pylib import const as t_const
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.util import to_positive_float as as_float
from traiter.rules.base import Base

FLOAT_RE: str = r"\d{1,4}(\.\d{,3})?"
FLOAT3_RE: str = r"\d{3}(\.\d{,3})?"
INT_RE: str = r"\d{1,4}"
DEC_RE: str = r"\.\d{1,3}"

FACT_LEN = 2

# This pipe is used multiple times
UNIQUE = 0  # A tiebreaker used to rename the Number pipe


@dataclass(eq=False)
class Number(Base):
    # Class vars ----------
    csv: ClassVar[Path] = Path(__file__).parent / "terms" / "number_word_terms.csv"
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(csv, "replace", int)
    # ---------------------

    number: float = None
    is_fraction: bool = None
    is_word: bool = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn()

    @classmethod
    def pipe(cls, nlp: Language, _overwrite: list[str] | None = None):
        global UNIQUE
        UNIQUE += 1

        add.term_pipe(nlp, name=f"number_terms_{UNIQUE}", path=cls.csv)

        add.trait_pipe(nlp, name=f"fraction_{UNIQUE}", compiler=cls.fraction_patterns())

        add.trait_pipe(
            nlp, name=f"number_word_{UNIQUE}", compiler=cls.number_word_patterns()
        )

        add.trait_pipe(nlp, name=f"number_{UNIQUE}", compiler=cls.number_patterns())
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
    def number_word_patterns(cls):
        decoder = {
            "word": {"ENT_TYPE": "number_word"},
        }
        return [
            Compiler(
                label="number",
                on_match="number_word_match",
                decoder=decoder,
                patterns=[
                    " word ",
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

        if numbers[-1] == 0:
            raise RejectMatch

        number = numbers[-2] / numbers[-1]  # Calculate the fraction part
        # Add in the whole number part
        number += numbers[0] if len(numbers) > FACT_LEN else 0.0

        trait = cls.from_ent(ent, number=number, is_fraction=True)

        ent[0]._.trait = trait
        ent[0]._.flag = "number"

        return trait

    @classmethod
    def number_word_match(cls, ent):
        word = ent.text.lower()
        number = cls.replace.get(word)

        trait = cls.from_ent(ent, number=number, is_word=True)

        ent[0]._.trait = trait
        ent[0]._.flag = "number"

        return trait


@registry.misc("number_match")
def number_match(ent):
    return Number.number_match(ent)


@registry.misc("number_word_match")
def number_word_match(ent):
    return Number.number_word_match(ent)


@registry.misc("fract_match")
def fract_match(ent):
    return Number.fract_match(ent)
