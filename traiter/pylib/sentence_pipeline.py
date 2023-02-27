from spacy.lang.en import English

from . import tokenizer
from .pipes.sentence_pipe import SENTENCE


def pipeline():
    nlp = English()
    tokenizer.setup_tokenizer(nlp)
    nlp.add_pipe(SENTENCE, config={"abbrev": tokenizer.ABBREVS})
    return nlp
