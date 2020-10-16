"""Common pipeline functions."""

import re
from typing import Dict, List

import spacy
from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER, \
    CONCAT_QUOTES, HYPHENS, LIST_ELLIPSES, LIST_ICONS
from spacy.tokens import Doc, Span, Token

if not Token.has_extension('data'):
    Token.set_extension('data', default={})
    Token.set_extension('step', default='')
    Span.set_extension('data', default={})
    Span.set_extension('step', default='')


class SpacyPipeline:
    """Build a custom traiter pipeline."""

    entities2keep = set()
    token2entity = set()

    def __init__(
            self,
            lang_model: str = 'en_core_web_sm',
            gpu: str = 'prefer',
            tokenizer: bool = True
    ) -> None:
        if gpu == 'prefer':
            spacy.prefer_gpu()
        elif gpu == 'require':
            spacy.require_gpu()

        self.nlp = spacy.load(lang_model)

        if tokenizer:
            self.setup_tokenizer()

    def setup_tokenizer(self) -> None:
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

        breaking = r"""[\[\]\\/()<>˂˃:;,.?"“”'×+-]"""

        prefix = re.compile(f'^{breaking}')
        self.nlp.tokenizer.prefix_search = prefix.search

        suffix = re.compile(f'{breaking}$')
        self.nlp.tokenizer.suffix_search = suffix.search

    def to_entities(self, doc: Doc) -> None:
        """Convert trait tokens into entities."""
        new_ents = []

        keep = set()  # Keep these entities

        for ent in doc.ents:
            if ent.label_ in self.entities2keep:
                new_ents.append(ent)
                keep |= {i for i in range(ent.start, ent.end)}

        for token in doc:
            if token.i in keep:
                continue

            if ent_type_ := token.ent_type_:
                if token._.step not in self.token2entity:
                    continue
                if token._.data.get('_skip'):
                    continue

                span = Span(doc, token.i, token.i + 1, label=ent_type_)

                span._.data = token._.data
                span._.step = token._.step

                new_ents.append(span)

        doc.ents = tuple(new_ents)

    def find_entities(self, text: str) -> Doc:
        """Find entities in the doc."""
        doc = self.nlp(text)
        self.to_entities(doc)
        return doc

    @staticmethod
    def trait_list(doc: Doc) -> List[Dict]:
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

    def test_traits(self, text: str) -> List[Dict]:
        """Build unit test data."""
        doc = self.find_entities(text)
        traits = self.trait_list(doc)

        # from pprint import pp
        # pp(traits)

        return traits
