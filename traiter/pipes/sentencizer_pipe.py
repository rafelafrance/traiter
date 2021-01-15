"""Custom sentence splitter."""

# pylint: disable=too-many-boolean-expressions, too-few-public-methods

from typing import List, Union

import regex
from spacy.tokens import Doc
from spacy.language import Language

PUNCT = ['SPACE', 'PUNCT']


class SentencizerPipe:
    """Shared sentencizer logic."""

    def __init__(
            self,
            abbrevs: Union[str, List[str]],
            headings: Union[str, List[str]] = ''
    ) -> None:
        """Build a custom sentencizer.

        Each client sentencizer has its own abbreviations that will prevent a
        sentence split.
        """
        abbrevs = abbrevs.split() if isinstance(abbrevs, str) else abbrevs
        abbrevs = '|'.join(abbrevs)
        self.abbrevs = regex.compile(fr'(?:{abbrevs})$')

        self.headings = headings.split() if isinstance(headings, str) else headings

    def __call__(self, doc: Doc) -> Doc:
        """Break the text into sentences."""
        for i, token in enumerate(doc[:-1]):
            prev = doc[i - 1] if i > 0 else None
            next_ = doc[i + 1]
            if (token.ent_type_ in self.headings
                    and (not prev or self.is_prev(prev))
                    and self.is_next(next_)):
                next_.is_sent_start = True
                token.is_sent_start = True
            elif (token.text == '.'
                    and prev and not self.abbrevs.match(prev.text)
                    and (len(prev) > 1 or self.is_prev(prev))
                    and (len(next_) > 1 or self.is_next(next_))):
                next_.is_sent_start = True
            elif (token.text == '.'
                    and self.is_prev(prev)
                    and self.is_next(next_)):
                next_.is_sent_start = True
            elif token.text in '"”\'' and prev and prev.text == '.':
                next_.is_sent_start = True
            else:
                next_.is_sent_start = False

        return doc

    @staticmethod
    def is_prev(token):
        """See if the surrounding token meets needed criteria."""
        return token.pos_ == 'SPACE' or token.text in ')].'

    @staticmethod
    def is_next(token):
        """See if the next token meets needed criteria."""
        return token.prefix_.isupper() or token.pos_ == 'SPACE' or token.text in '.'

    @classmethod
    def add_pipe(
            cls,
            nlp: Language,
            abbrevs: Union[str, List[str]],
            headings: Union[str, List[str]] = '',
            **kwargs
    ) -> None:
        """Add entities converter to the pipeline."""
        kwargs = {'before': 'parser'} if not kwargs else kwargs
        pipe = cls(abbrevs=abbrevs, headings=headings)
        nlp.add_pipe(pipe, **kwargs)
