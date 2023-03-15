import spacy

from .pattern_compilers.matcher import Compiler
from .patterns import color
from .patterns import date_
from .patterns import habitat
from .patterns import lat_long
from .pipes import debug
from .pipes.add import ADD_TRAITS
from .pipes.delete import DELETE_TRAITS
from .pipes.merge import MERGE_TRAITS
from .pipes.term import TERM_PIPE


class PipelineBuilder:
    def __init__(self, trained_pipeline="en_core_web_sm", exclude=None):
        exclude = exclude if exclude is not None else []
        exclude = exclude if isinstance(exclude, list) else [exclude]
        self.nlp = spacy.load(trained_pipeline, exclude=exclude)
        self.spacy_ent_labels = self.nlp.meta["labels"].get("ner", [])

    def __call__(self, text):
        return self.nlp(text)

    def terms(self, terms, replace=None, merge=True, **kwargs):
        replace = replace if replace else {}
        self.nlp.add_pipe(
            TERM_PIPE,
            before="parser",
            **kwargs,
            config={"terms": terms.data, "replace": replace},
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

    def color(self, **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name="color",
            **kwargs,
            config={"patterns": Compiler.as_dicts([color.COLOR])},
        )

    def date_(self, **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name="date",
            **kwargs,
            config={"patterns": Compiler.as_dicts([date_.DATE, date_.MISSING_DAY])},
        )

    def habitat(self, **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name="habitat",
            **kwargs,
            config={"patterns": Compiler.as_dicts([habitat.HABITAT])},
        )

    def lat_long(self, **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name="lat_long",
            **kwargs,
            config={"patterns": Compiler.as_dicts([lat_long.LAT_LONG])},
        )

    def delete_traits(self, traits, name=DELETE_TRAITS, **kwargs):
        self.nlp.add_pipe(DELETE_TRAITS, name=name, **kwargs, config={"delete": traits})

    def merge(self, **kwargs):
        self.nlp.add_pipe(MERGE_TRAITS, **kwargs)

    def add_debug_ents_pipe(self):
        debug.ents(self.nlp)

    def add_debug_tokens_pipe(self):
        debug.tokens(self.nlp)
