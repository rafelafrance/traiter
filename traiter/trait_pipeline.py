"""Common pipeline functions."""

from .spacy_nlp import to_entities


class TraitPipeline:
    """Build a custom traiter pipeline."""

    steps2link = None

    def __init__(self, nlp):
        self.nlp = nlp

    def find_entities(self, text):
        """Find entities in the doc."""
        doc = self.nlp(text)
        to_entities(doc, steps=self.steps2link)
        return doc

    @staticmethod
    def trait_list(doc):
        """Tests require a trait list."""
        traits = []

        for ent in doc.ents:
            data = {k: v for k, v in ent._.data.items()
                    if not k.startswith('_')}
            data['trait'] = ent.label_
            data['start'] = ent.start_char
            data['end'] = ent.end_char
            traits.append(data)

        return traits

    def test_traits(self, text):
        """Build unit test data."""
        doc = self.find_entities(text)
        traits = self.trait_list(doc)

        # from pprint import pp
        # pp(traits)

        return traits
