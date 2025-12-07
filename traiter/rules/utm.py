import re
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.tokens import Span
from spacy.util import registry

from traiter.pipes import add
from traiter.pylib import const, term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.rules.rule import Rule


@dataclass(eq=False)
class UTM(Rule):
    # Class vars ----------
    sym: ClassVar[str] = r"""°"”“'`‘´’"""
    punct: ClassVar[str] = f"""{sym},;._"""
    datum_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "datum_terms.csv"
    utm_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "utm_terms.csv"
    unit_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "unit_length_terms.csv"
    all_csvs: ClassVar[list[Path]] = [utm_csv, datum_csv, unit_csv]
    replace: ClassVar[dict[str, str]] = term_util.look_up_table(all_csvs, "replace")
    dir_: ClassVar[str] = """((north|east|south|west)(ing)?|[nesw])"""
    # ---------------------

    utm: str | None = None
    datum: str | None = None

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        add.term_pipe(nlp, name="utm_terms", path=cls.all_csvs)
        add.trait_pipe(nlp, name="utm_patterns", compiler=cls.utm_patterns())
        add.cleanup_pipe(nlp, name="utm_cleanup")

    @classmethod
    def utm_patterns(cls) -> list[Compiler]:
        decoder = {
            "(": {"TEXT": {"IN": const.OPEN}},
            ")": {"TEXT": {"IN": const.CLOSE}},
            ",": {"TEXT": {"REGEX": r"^[,;._:]\Z"}},
            "99": {"LOWER": {"REGEX": r"^\d{1,3}$"}},
            "9999": {"LOWER": {"REGEX": r"^\d+$"}},
            "datum": {"ENT_TYPE": "datum"},
            "datum_label": {"ENT_TYPE": "datum_label"},
            "sect": {"LOWER": {"REGEX": r"""^(section|sec\.?|s)$"""}},
            "uaa": {"LOWER": {"REGEX": r"^u[a-z]{1,2}$"}},
            "uncert": {"ENT_TYPE": "uncertain_label"},
            "utm_dir": {"LOWER": {"REGEX": rf"""^{cls.dir_}\Z"""}},
            "utm_label": {"ENT_TYPE": "utm_label"},
        }
        return [
            Compiler(
                label="utm",
                decoder=decoder,
                on_match="utm_match",
                patterns=[
                    "utm_label* 99 sect ,* 9999 utm_dir? ,* 9999 utm_dir? (? datum* )?",
                    "utm_label+ 99 ,* 9999 utm_dir? ,* 9999 utm_dir? (? datum* )?",
                    "99 uaa 9999",
                ],
            ),
        ]

    @classmethod
    def format_coords(cls, frags: list[str]) -> str:
        coords = " ".join(frags)
        coords = re.sub(rf"\s([{cls.punct}])", r"\1", coords)
        coords = re.sub(r"\s(:)", r"\1", coords)
        coords = re.sub(r"(?<=\d)([NESWnesw])", r" \1", coords)
        coords = re.sub(r"-\s(?=\d)", r"-", coords)
        return " ".join(coords.split())

    @classmethod
    def utm_match(cls, ent: Span) -> "UTM":
        frags = []
        datum = []

        for token in ent:
            if token.ent_type_ == "utm_label":
                continue

            if token.text in const.OPEN + const.CLOSE:
                continue

            if token.ent_type_ == "datum":
                datum.append(token.lower_)

            else:
                text = token.text.upper() if len(token.text) == 1 else token.text
                frags.append(text)

        if datum:
            datum = "".join(datum)
            datum = cls.replace.get(datum, datum)
        else:
            datum = None

        utm = cls.format_coords(frags)

        return cls.from_ent(ent, utm=utm, datum=datum)


@registry.misc("utm_match")
def utm_match(ent: Span) -> UTM:
    return UTM.utm_match(ent)
