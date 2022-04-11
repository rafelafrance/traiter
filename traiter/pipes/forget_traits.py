"""Remove noise partial traits from the doc."""
from spacy import registry
from spacy.language import Language
from spacy.tokens import Doc

FORGET_TRAITS = "traiter.forget_partial_traits.v1"


@Language.factory(FORGET_TRAITS)
class ForgetTraits:
    """Remove partial traits.

    Traits are built up in layers and sometimes a partial trait in a lower layer is
    not used in an upper layer. This will cause noisy output, so we remove them.
    """

    def __init__(
        self, nlp: Language, name: str, forget: list[str] = None, forget_when: str = ""
    ):
        super().__init__()
        self.nlp = nlp
        self.name = name
        self.forget = forget if forget else []
        if forget_when:
            self.forget_when = registry.misc.get(forget_when)
        else:
            self.forget_when = lambda _: False

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        for ent in doc.ents:
            if ent.label_ in self.forget or self.forget_when(ent):
                continue
            entities.append(ent)

        doc.ents = entities
        return doc
