"""Custom sentence splitter."""

from typing import List, Optional

import regex
from spacy.language import Language
from spacy.tokens import Doc


@Language.factory('sentence')
def sentence(
        nlp: Language,
        name: str,
        abbrevs: Optional[List[str]] = None,
        headings: Optional[List[str]] = None):
    """Create a sentence pipe."""
    return Sentence(abbrevs, headings)


class Sentence:
    """Shared sentencizer logic."""

    def __init__(
            self,
            abbrevs: Optional[List[str]] = None,
            headings: Optional[List[str]] = None
    ) -> None:
        """Build a custom sentencizer.

        Each client sentencizer has its own abbreviations that will prevent a
        sentence split.
        """
        abbrevs = abbrevs if abbrevs else []
        abbrevs = '|'.join(abbrevs)
        self.abbrevs = regex.compile(fr'(?:{abbrevs})$')
        self.headings = headings if headings else []

    def __call__(self, doc: Doc) -> Doc:
        """Break the text into sentences."""
        for i, token in enumerate(doc[:-1]):
            prev = doc[i - 1] if i > 0 else None
            next_ = doc[i + 1]
            # Document headings like "Introduction" are a separate sentence
            if (token.ent_type_ in self.headings
                    and (not prev or self.is_prev(prev))
                    and self.is_next(next_)):
                next_.is_sent_start = True
                token.is_sent_start = True
            # A sentence if the previous token is not an abbreviation
            elif (token.text == '.'
                  and prev and not self.abbrevs.match(prev.text)
                  and (len(prev) > 1 or self.is_prev(prev))
                  and (len(next_) > 1 or self.is_next(next_))):
                next_.is_sent_start = True
            #
            elif (token.text == '.'
                  and self.is_prev(prev)
                  and self.is_next(next_)):
                next_.is_sent_start = True
            # Capture sentences inside of quotes
            elif token.text in '"”\'' and prev and prev.text == '.':
                next_.is_sent_start = True
            else:
                next_.is_sent_start = False

        return doc

    @staticmethod
    def is_prev(token):
        """See if the previous toke is a space or a bracket."""
        return token.pos_ == 'SPACE' or token.text in ')].'

    @staticmethod
    def is_next(token):
        """See if the next token starts with an uppercase is a space or period."""
        return token.prefix_.isupper() or token.pos_ == 'SPACE' or token.text in '.'
