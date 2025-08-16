import re
from dataclasses import dataclass
from typing import ClassVar

from spacy import Language, registry

from traiter.pipes import add, reject_match
from traiter.pylib import const as t_const
from traiter.pylib.pattern_compiler import Compiler
from traiter.rules.base import Base


@dataclass(eq=False)
class Uuid(Base):
    # Class vars ----------
    hx: ClassVar[str] = "[0-9A-Fa-f]"
    whole: ClassVar[str] = rf"^{hx}{{8}}-{hx}{{4}}-{hx}{{4}}-{hx}{{4}}-{hx}{{12}}$"
    # ---------------------

    uuid: str = None

    @classmethod
    def pipe(cls, nlp: Language, _overwrite: list[str] | None = None):
        # add.debug_tokens(nlp)  # ###########################################
        add.trait_pipe(nlp, name="uuid_patterns", compiler=cls.uuid_patterns())

    @classmethod
    def uuid_patterns(cls):
        decoder = {
            "-": {"TEXT": {"IN": t_const.DASH}},
            "hex": {"LOWER": {"REGEX": f"^{cls.hx}+$"}, "OP": "+"},
        }
        return [
            Compiler(
                label="uuid",
                on_match="uuid_match",
                decoder=decoder,
                patterns=[
                    " hex - hex - hex - hex - hex ",
                ],
            ),
        ]

    @classmethod
    def uuid_match(cls, ent):
        if not re.search(cls.whole, ent.text):
            raise reject_match.SkipTraitCreation
        return super().from_ent(ent, uuid=ent.text)


@registry.misc("uuid_match")
def uuid_match(ent):
    return Uuid.uuid_match(ent)
