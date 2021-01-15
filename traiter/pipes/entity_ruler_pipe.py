"""Add an entity ruler to the pipeline."""

from spacy.language import Language
from spacy.pipeline import EntityRuler

from traiter.patterns import Patterns


class EntityRulerPipe:
    """Entity ruler for the pipeline."""

    @classmethod
    def add_pipe(
            cls,
            nlp: Language,
            patterns: Patterns,
            *,
            attr: str = 'LOWER',
            name: str = 'entity_ruler',
            **kwargs
    ) -> None:
        """Build rule matchers that recognize traits."""
        kwargs = {'before': 'parser'} if not kwargs else kwargs
        ruler = EntityRuler(nlp, phrase_matcher_attr=attr, overwrite_ents=True)
        ruler.add_patterns(patterns.for_ruler())
        nlp.add_pipe(ruler, name=name, **kwargs)
