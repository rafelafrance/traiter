import spacy

from traiter.pipes import extensions, sentence, tokenizer
from traiter.pylib.rules.color import Color
from traiter.pylib.rules.date_ import Date
from traiter.pylib.rules.elevation import Elevation
from traiter.pylib.rules.habitat import Habitat
from traiter.pylib.rules.lat_long import LatLong
from traiter.pylib.rules.trs import TRS
from traiter.pylib.rules.utm import UTM
from traiter.pylib.rules.uuid import Uuid


def build():
    extensions.add_extensions()

    nlp = spacy.load("en_core_web_md", exclude=["ner"])

    tokenizer.setup_tokenizer(nlp)

    nlp.add_pipe(sentence.SENTENCES, before="parser")

    Color.pipe(nlp)
    Uuid.pipe(nlp)
    Date.pipe(nlp)
    Elevation.pipe(nlp)
    LatLong.pipe(nlp)
    Habitat.pipe(nlp)
    TRS.pipe(nlp)
    UTM.pipe(nlp)

    return nlp
