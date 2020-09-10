"""Common pipeline functions."""

from spacy.tokens import Span


class TraitPipeline:
    """Build a custom traiter pipeline."""

    steps2link = None

    def __init__(self, nlp):
        self.nlp = nlp

    def to_entities(self, doc):
        """Convert trait tokens into entities."""
        spans = []
        for token in doc:
            if ent_type_ := token.ent_type_:
                if self.steps2link and token._.step not in self.steps2link:
                    continue
                if token._.data.get('_skip'):
                    continue
                data = {k: v for k, v in token._.data.items()}

                span = Span(doc, token.i, token.i + 1, label=ent_type_)

                span._.data = data
                span._.step = token._.step

                spans.append(span)

        doc.ents = spans

    def find_entities(self, text):
        """Find entities in the doc."""
        doc = self.nlp(text)
        self.to_entities(doc)
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
