from traiter.pylib import pipeline
from traiter.pylib.util import shorten

PIPELINE = pipeline.build()

# from traiter.pylib.const import MODEL_PATH
# PIPELINE = pipeline.build(MODEL_PATH)
# PIPELINE = pipeline.load(MODEL_PATH)


def test(text: str) -> list[dict]:
    text = shorten(text)
    doc = PIPELINE(text)
    traits = [e._.data for e in doc.ents]

    # from pprint import pp
    # pp(traits, compact=True)

    return traits
