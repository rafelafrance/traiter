from spacy.lang.en import English

from .old import tokenizer
from .pipes.sentence import SENTENCE


def pipeline():
    nlp = English()
    tokenizer.setup_tokenizer(nlp)
    nlp.add_pipe(SENTENCE, config={"abbrev": tokenizer.ABBREVS})
    return nlp
