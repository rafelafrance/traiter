"""Split matchers for the pipeline.

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

The match action returns a list of data dicts that must contain a "_start" and "_end"
token offsets within the span.
"""

from spacy.tokens import Doc

from .rule import Rule


class Split(Rule):
    """Split matchers for the pipeline."""

    def __call__(self, doc: Doc) -> Doc:
        """Find all term in the text and return the resulting doc."""
        spans = self.get_spans(doc)

        with doc.retokenize() as retokenizer:
            for span in spans:
                label = span.label_
                action = self.actions.get(label)
                data = action(span) if action else []

                if not data:
                    continue

                label = label.split('.')[0]

                for datum in data:
                    new_label = datum['_label'] if datum.get('_label') else label

                    attrs = {'ENT_TYPE': new_label, 'ENT_IOB': 3,
                             '_': {'data': datum, 'step': self.step}}

                    frag = span[datum['_start']:datum['_end']]

                    retokenizer.merge(frag, attrs=attrs)

        self.debug(doc)
        return doc
