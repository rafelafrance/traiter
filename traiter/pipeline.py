"""Common pipeline functions."""

from .spacy_nlp import to_entities


class Pipeline:
    """Build a custom traiter pipeline."""

    steps2link = None

    def __init__(self, nlp, linker=None):
        self.nlp = nlp
        self.linker = linker

    def ner(self, text):
        """Find entities in the doc."""
        doc = self.nlp(text)

        if self.linker:
            for sent in doc.sents:
                self.linker(sent)

        to_entities(doc, steps=self.steps2link)
        return doc

    def trait_list(self, text):
        """Tests require a trait list."""
        doc = self.ner(text)

        traits = []

        for ent in doc.ents:
            data = ent._.data
            data['trait'] = ent.label_
            data['start'] = ent.start_char
            data['end'] = ent.end_char
            traits.append(data)

        # from pprint import pp
        # pp(traits)

        return traits
