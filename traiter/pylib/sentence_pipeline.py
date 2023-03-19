from spacy.lang.en import English

from .pipes.sentence import SENTENCE


def pipeline(base_model="en_core_web_sm"):
    nlp = English()
    nlp.add_pipe(SENTENCE, config={"base_model": base_model})
    return nlp
