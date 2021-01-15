"""Rule matchers for the pipeline."""

from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc, Span
from spacy.util import filter_spans

from traiter.patterns import Patterns, PatternMatcherType


class MatcherPipe:
    """A matchers that retokenizes the matches."""

    # We sometimes want to process the same trait name with different actions.
    # This is a tiebreaker for trait names. For instance, we may want to process
    # sizes like "10 m long" differently from "10-15 m long" even though they're
    # both size traits.
    count: int = 0

    def __init__(self, nlp: Language, patterns: PatternMatcherType) -> None:
        self.matcher = Matcher(nlp.vocab)
        for label, rules in patterns.items():
            self.matcher.add(label, rules)

    def __call__(self, doc: Doc) -> Doc:
        """Find all matches in the text and return the resulting doc.

        All non-overlapping matches are added. Also, all previous entities that do not
        overlap with a new match are kept.
        """
        # self.debug(doc)

        matches = self.matcher(doc)
        spans = [Span(doc, s, e, label=i) for i, s, e in matches]
        spans = filter_spans(spans)

        seen = set()
        for span in spans:
            seen.update(range(span.start, span.end))

        for ent in doc.ents:
            if ent.start not in seen and ent.end - 1 not in seen:
                spans.append(ent)
                seen.update(range(ent.start, ent.end))

        spans = sorted(spans, key=lambda s: s.start)

        doc.ents = tuple(spans)
        return doc

    @staticmethod
    def debug(doc):
        """Print debug messages."""
        print('-' * 80)
        for token in doc:
            print(f'{token.ent_type_:<20} {token.pos_:<6} {token}')
        print()

    @classmethod
    def add_pipe(
            cls, nlp: Language, patterns: Patterns, name: str, **kwargs
    ) -> None:
        """Build rule matchers that recognize traits."""
        kwargs = {'before': 'parser'} if not kwargs else kwargs
        matcher = cls(nlp, patterns.for_matcher())
        nlp.add_pipe(matcher, name=name, **kwargs)
