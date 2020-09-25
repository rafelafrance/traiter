"""Common pipeline functions."""

import re

import spacy
from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER, \
    CONCAT_QUOTES, HYPHENS, LIST_ELLIPSES, LIST_ICONS
from spacy.tokens import Span, Token

if not Token.has_extension('data'):
    Token.set_extension('data', default={})
    Token.set_extension('step', default='')
    Span.set_extension('data', default={})
    Span.set_extension('step', default='')


class SpacyPipeline:
    """Build a custom traiter pipeline."""

    steps2link = None

    def __init__(self, lang_model='en_core_web_sm', gpu='prefer'):
        if gpu == 'prefer':
            spacy.prefer_gpu()
        elif gpu == 'require':
            spacy.require_gpu()
        self.nlp = spacy.load(lang_model)
        self.setup_tokenizer()

    def setup_tokenizer(self):
        """Setup custom tokenizer rules for the pipeline."""
        infix = (
                LIST_ELLIPSES
                + LIST_ICONS
                + [
                    r"(?<=[0-9])[+\-\*^](?=[0-9])",
                    r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
                        al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES),
                    r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
                    # r"(?<=[{a}])(?:{h})(?=[{a}])".format(a=ALPHA, h=HYPHENS),
                    r"(?<=[{a}0-9])[:<>=/+](?=[{a}])".format(a=ALPHA),
                    r"""(?:{h})+""".format(h=HYPHENS),
                    r"""[\\\[\]\(\)/:;"“”'+]""",
                    r"(?<=[0-9])\.?(?=[{a}])".format(a=ALPHA),  # 1.word or 1N
                ])

        infix_regex = spacy.util.compile_infix_regex(infix)
        self.nlp.tokenizer.infix_finditer = infix_regex.finditer

        breaking = r"""[\[\]\\/()<>˂˃:;,.?"“”'+-]"""

        prefix = re.compile(f'^{breaking}')
        self.nlp.tokenizer.prefix_search = prefix.search

        suffix = re.compile(f'{breaking}$')
        self.nlp.tokenizer.suffix_search = suffix.search

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
