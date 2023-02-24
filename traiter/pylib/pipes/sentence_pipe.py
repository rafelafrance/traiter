"""Custom sentence splitter."""
from typing import Optional

from spacy.language import Language
from spacy.tokens import Doc

from .. import const

SENTENCE = "traiter_sentence_v1"

EOS = """ . ? ! … """.split()  # End Of Sentence
PREV_EOS = const.CLOSE + EOS

QUOTES = set(const.QUOTE)
QUOTES.discard(",")


@Language.factory(SENTENCE)
class Sentence:
    def __init__(
        self,
        nlp: Language,
        name: str,
        abbrev: Optional[list[str]] = None,
    ):
        self.nlp = nlp
        self.name = name
        self.abbrev = set(abbrev) if abbrev else set()

    def __call__(self, doc: Doc) -> Doc:
        for i, token in enumerate(doc[:-1]):
            prev = doc[i - 1] if i > 0 else None
            next_ = doc[i + 1]

            # A period followed by a something that allows a sentence start
            if (
                token.text.endswith(".")
                and self.allows_new_sentence(next_)
                and token.text not in self.abbrev
            ):
                next_.is_sent_start = True

            # Quotes preceded by a period
            elif token.text in QUOTES and prev and prev.text in EOS:
                next_.is_sent_start = True

            # Not a sentence break
            else:
                next_.is_sent_start = False

        return doc

    @staticmethod
    def is_space(token):
        """Check if the token is space."""
        return token.text.isspace() or token.pos_ == "SPACE"

    def allows_new_sentence(self, token):
        """See if the next token does not block a sentence start."""
        return (
            token.prefix_.isupper()
            or token.prefix_.isdigit()
            or self.is_space(token)
            or token.text in EOS
        )