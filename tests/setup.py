from traiter.pylib.pipeline import pipeline
from traiter.pylib.util import shorten

PIPELINE = pipeline()


def test(text: str) -> list[dict]:
    text = shorten(text)
    doc = PIPELINE(text)
    traits = [e._.data for e in doc.ents]

    # from pprint import pp
    # pp(traits, compact=True)

    return traits
