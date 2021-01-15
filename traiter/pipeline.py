"""Common pipeline functions."""

import re
from typing import Dict, List

import spacy
from spacy.lang.char_classes import (
    ALPHA, ALPHA_LOWER, ALPHA_UPPER, CONCAT_QUOTES, HYPHENS, LIST_ELLIPSES, LIST_ICONS)
from spacy.tokens import Doc, Span, Token

# Custom fields attached to tokens and spans
# data:      Attach data specific to the trait in this dict
# prev_label: A token's original label_ which is set when during retokenization
# action:    Used to pass commands from callback (actions) to the pipe
if not Span.has_extension('data'):
    Span.set_extension('data', default={})
    Span.set_extension('prev_label', default='')
    Span.set_extension('new_label', default='')
    Token.set_extension('data', default={})
    Token.set_extension('prev_label', default='')
    Token.set_extension('new_label', default='')


class SpacyPipeline:
    """Build a custom traiter pipeline."""

    def __init__(
            self,
            lang_model: str = 'en_core_web_sm',
            gpu: str = 'prefer',
            tokenizer: bool = True,
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
        # The default Spacy tokenizer works great for model-based parsing but
        # causes trouble with rule-based parsers.
        infix = (
                LIST_ELLIPSES
                + LIST_ICONS
                + [
                    r'(?<=[0-9])[+\-\*^](?=[0-9])',
                    r'(?<=[{al}{q}])\.(?=[{au}{q}])'.format(
                        al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES
                    ),
                    r'(?<=[{a}]),(?=[{a}])'.format(a=ALPHA),
                    r'(?<=[{a}0-9])[:<>=/+](?=[{a}])'.format(a=ALPHA),
                    r"""(?:{h})+""".format(h=HYPHENS),
                    r"""[\\\[\]\(\)/:;’'“”'+]""",
                    r'(?<=[0-9])\.?(?=[{a}])'.format(a=ALPHA),  # 1.word or 1N
                    r'(?<=[{a}]),(?=[0-9])'.format(a=ALPHA),  # word,digits
                ]
        )

        infix_regex = spacy.util.compile_infix_regex(infix)
        self.nlp.tokenizer.infix_finditer = infix_regex.finditer

        breaking = r"""[\[\]\\/()<>˂˃:;,.?"“”'’×+~-]"""

        prefix = re.compile(f'^{breaking}')
        self.nlp.tokenizer.prefix_search = prefix.search

        suffix = re.compile(f'{breaking}$')
        self.nlp.tokenizer.suffix_search = suffix.search

    @staticmethod
    def trait_list(doc: Doc) -> List[Dict]:
        """Tests require a trait list."""
        traits = []

        for ent in doc.ents:
            data = {k: v for k, v in ent._.data.items()}
            traits.append(data)

        return traits

    def test_traits(self, text: str) -> List[Dict]:
        """Build unit test data."""
        doc = self.nlp(text)

        traits = self.trait_list(doc)

        # from pprint import pp
        # pp(traits)

        return traits
