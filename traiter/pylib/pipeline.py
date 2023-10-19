import spacy

from traiter.pylib.pipes import extensions, sentence, tokenizer
from traiter.pylib.traits.color import Color
from traiter.pylib.traits.date_ import Date
from traiter.pylib.traits.elevation import Elevation
from traiter.pylib.traits.habitat import Habitat
from traiter.pylib.traits.lat_long import LatLong
from traiter.pylib.traits.trs import TRS
from traiter.pylib.traits.utm import UTM


def build():
    extensions.add_extensions()

    nlp = spacy.load(
        "en_core_web_sm",
        exclude=["ner", "lemmatizer", "tok2vec"],
    )

    tokenizer.setup_tokenizer(nlp)

    nlp.add_pipe(sentence.SENTENCES, before="parser")

    Color.pipe(nlp)
    Date.pipe(nlp)
    Elevation.pipe(nlp)
    LatLong.pipe(nlp)
    Habitat.pipe(nlp)
    TRS.pipe(nlp)
    UTM.pipe(nlp)

    return nlp
