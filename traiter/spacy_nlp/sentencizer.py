"""Custom sentence splitter."""

# pylint: disable=too-many-boolean-expressions, too-few-public-methods

from typing import List, Union

import regex
from spacy.tokens import Doc


class SpacySentencizer:
    """Shared sentencizer logic."""

    def __init__(self, abbrevs: Union[str, List[str]]) -> None:
        """Build a custom sentencizer.

        Each client sentencizer has its own abbreviations that will prevent a
        sentence split.
        """
        abbrevs = abbrevs.split() if isinstance(abbrevs, str) else abbrevs
        abbrevs = '|'.join(abbrevs)
        self.abbrevs = regex.compile(fr'(?:{abbrevs})$')

    def __call__(self, doc: Doc) -> Doc:
        """Break the text into sentences."""
        for i, token in enumerate(doc[:-1]):
            prev_token = doc[i - 1] if i > 0 else None
            next_token = doc[i + 1]
            if (token.text == '.' and regex.match(r'[A-Z]', next_token.prefix_)
                    and not self.abbrevs.match(next_token.text) and prev_token
                    and len(next_token) > 1 and len(prev_token) > 1):
                next_token.is_sent_start = True
            elif (token.text in '"”\''
                  and prev_token and prev_token.text == '.'):
                next_token.is_sent_start = True
            else:
                next_token.is_sent_start = False

        return doc
