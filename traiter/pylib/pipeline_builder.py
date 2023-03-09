import spacy

from . import tokenizer
from .pattern_compilers import matcher_compiler
from .patterns import color_patterns
from .patterns import habitat_patterns
from .pipes import debug_pipes
from .pipes.add_traits_pipe import ADD_TRAITS
from .pipes.delete_traits_pipe import DELETE_TRAITS
from .pipes.merge_traits import MERGE_TRAITS
from .pipes.term_pipe import TERM_PIPE


class PipelineBuilder:
    def __init__(self, trained_pipeline="en_core_web_sm", exclude=None):
        exclude = exclude if exclude is not None else []
        exclude = exclude if isinstance(exclude, list) else [exclude]
        self.nlp = spacy.load(trained_pipeline, exclude=exclude)
        self.spacy_ent_labels = self.nlp.meta["labels"].get("ner", [])

    def __call__(self, text):
        return self.nlp(text)

    def add_tokenizer_pipe(self):
        tokenizer.setup_tokenizer(self.nlp)

    def add_term_patterns(self, terms, replace=None, merge=True, **kwargs):
        replace = replace if replace else {}
        self.nlp.add_pipe(
            TERM_PIPE,
            before="parser",
            **kwargs,
            config={"terms": terms, "replace": replace},
        )
        if merge:
            self.nlp.add_pipe("merge_entities", name="merge_terms", after=TERM_PIPE)

    def remove_spacy_ents(self, keep, **kwargs):
        keep = keep.split() if isinstance(keep, str) else keep
        keep = [k.upper() for k in keep]
        labels = [lb for lb in self.spacy_ent_labels if lb not in keep]
        self.nlp.add_pipe(
            DELETE_TRAITS,
            name="delete_spacy",
            **kwargs,
            config={"delete": labels},
        )

    def add_color_patterns(self, **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name="color_patterns",
            **kwargs,
            config={"patterns": matcher_compiler.as_dicts([color_patterns.COLOR])},
        )

    def add_habitat_patterns(self, **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name="habitat_patterns",
            **kwargs,
            config={"patterns": matcher_compiler.as_dicts([habitat_patterns.HABITAT])},
        )

    def add_delete_traits_patterns(self, traits, name=DELETE_TRAITS, **kwargs):
        self.nlp.add_pipe(DELETE_TRAITS, name=name, **kwargs, config={"delete": traits})

    def add_merge_pipe(self, **kwargs):
        self.nlp.add_pipe(MERGE_TRAITS, **kwargs)

    def add_debug_ents_pipe(self):
        debug_pipes.ents(self.nlp)

    def add_debug_tokens_pipe(self):
        debug_pipes.tokens(self.nlp)
