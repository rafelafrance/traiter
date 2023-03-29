import spacy

from . import tokenizer
from .pipes import extensions
from .pipes.finish import FINSH
from .pipes.sentence import SENTENCES
from .traits.color import color_pipe
from .traits.date import date_pipe
from .traits.elevation import elevation_pipe
from .traits.habitat import habitat_pipe
from .traits.lat_long import lat_long_pipe


def pipeline():
    extensions.add_extensions()

    nlp = spacy.load("en_core_web_sm", exclude=["ner", "parser"])

    tokenizer.setup_tokenizer(nlp)

    color_pipe.pipe(nlp)
    date_pipe.pipe(nlp)
    elevation_pipe.pipe(nlp)
    habitat_pipe.pipe(nlp)
    lat_long_pipe.pipe(nlp)

    nlp.add_pipe(SENTENCES)
    nlp.add_pipe(FINSH)

    # pipes.debug_tokens()  # #########################################

    # for name in nlp.pipe_names:
    #     print(name)

    return nlp
