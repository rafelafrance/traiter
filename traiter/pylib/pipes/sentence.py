"""Break text into sentences.

Experimental: Try using an agreement of both the dependency-based and statistical
sentence recognizers.
"""
import spacy
from spacy.language import Language
from spacy.tokens import Doc


SENTENCE = "traiter_sentence_v2"


@Language.factory(SENTENCE)
class Sentence:
    def __init__(self, nlp: Language, name: str, base_model: str = "en_core_web_sm"):
        self.nlp = nlp
        self.name = name

        self.nlp_d = spacy.load(base_model, exclude=["ner"])

        self.nlp_s = spacy.load(base_model, exclude=["parser", "ner"])
        self.nlp_s.enable_pipe("senter")

    def __call__(self, doc: Doc) -> Doc:
        # Workaround needed for spacy because setting 0 by itself does not work
        doc[-1].is_sent_start = False

        doc_d = self.nlp_d(doc.text)
        doc_s = self.nlp_s(doc.text)

        starts_d = {s.start for s in doc_d.sents}
        starts_s = {s.start for s in doc_s.sents}

        agree = starts_d & starts_s

        for i in agree:
            doc[i].is_sent_start = True

        return doc
