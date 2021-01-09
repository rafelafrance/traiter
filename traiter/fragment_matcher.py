"""Fragment matchers for the pipeline.

WARNING: THIS IS EXPERIMENTAL AND MAY GO AWAY. I.e. statistical matchers may be better
at this task (What about training data?). Or I may come up with a better idea later.

The idea here is that it is to make it possible to break one match into several traits.
The original use case is that some text may be a description trait but only if it's
next to another. The base rule matcher will only match the entire span as a single
trait.

For instance: "antennae unmodified in males;"

Could be broken down in several ways but for our purposes we want to keep the body part
trait, "antennae", and get its description, "unmodified in males", but without being
overly specific about what a description contains.

The match action returns a list of data dicts that must contain a _start and _end token
offset within the span.
"""

from spacy.tokens import Doc, Span
from spacy.util import filter_spans

from .rule_matcher import RuleMatcher


class FragmentMatcher(RuleMatcher):
    """Fragment matchers for the pipeline."""

    def __call__(self, doc: Doc) -> Doc:
        """Find all term in the text and return the resulting doc."""
        matches = self.matcher(doc)

        spans = [Span(doc, s, e, label=i) for i, s, e in matches]
        spans = filter_spans(spans)

        with doc.retokenize() as retokenizer:
            for span in spans:
                label = span.label_
                action = self.actions.get(label)
                data = action(span) if action else []

                if not data:
                    continue

                label = label.split('.')[0]

                for datum in data:
                    label = datum['_label'] if datum.get('_label') else label

                    attrs = {'ENT_TYPE': label, 'ENT_IOB': 3,
                             '_': {'data': datum, 'step': self.step}}

                    frag = span[datum['_start']:datum['_end']]

                    retokenizer.merge(frag, attrs=attrs)

        # print('-' * 80)
        # print(self.step)
        # for token in doc:
        #     print(f'{token.ent_type_:<15} {token._.step:<8} {token.pos_:<6} {token}')
        # print()

        return doc
