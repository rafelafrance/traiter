"""Tokens built by the scanner and used by the ruler and matcher."""

from sys import intern
from typing import List
import regex  # type: ignore


class Token:
    """The what we need to handle scanned words, numbers, puctuation, etc."""

    def __init__(self, text, **kwargs):
        self.text = intern(text)
        self.genus: str = kwargs.get('genus', '')
        self.canon = intern(self.cononical(self.text))
        self.start: int = kwargs.get('start', 0)
        self.end: int = kwargs.get('end', 0)
        # self.lemma = None           # The lemma
        # self.pos = None             # The part of speech
        # self.ocr                    # A normalization for OCR errors
        # self.x                      # Physical location on page
        # self.y                      # Physical location on page

    def __eq__(self, other):
        """Compare tokens."""
        return self.__dict__ == other.__dict__

    def __repr__(self) -> str:
        """Create string form of the object."""
        return '{}({})'.format(self.__class__.__name__, self.__dict__)

    def __getitem__(self, item):
        """Get an attribute using dict notation."""
        return getattr(self, item)

    def cononical(self, text):
        """Lower case the string & remove noise characters."""
        text = text.lower()
        if self.genus == 'word':
            text = regex.sub(r'\p{Dash_Punctuation}', '', text)
        return text


Tokens = List[Token]
