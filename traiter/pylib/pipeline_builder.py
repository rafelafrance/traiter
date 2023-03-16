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

    def terms(self, terms, name=TERM_PIPE, replace=None, merge=True, **kwargs):
        replace = replace if replace else {}
        self.nlp.add_pipe(
            TERM_PIPE,
            name=name,
            **kwargs,
            config={"terms": terms.data, "replace": replace},
        )
        if merge:
            self.nlp.add_pipe("merge_entities", name=f"{name}_merge", after=name)

    def delete_spacy_ents(self, name="delete_spacy", keep=None, **kwargs):
        keep = keep if keep else []
        keep = keep.split() if isinstance(keep, str) else keep
        keep = [k.upper() for k in keep]
        labels = [lb for lb in self.spacy_ent_labels if lb not in keep]
        self.nlp.add_pipe(
            DELETE_TRAITS,
            name=name,
            **kwargs,
            config={"delete": labels},
        )

    def colors(self, name="color", **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name=name,
            **kwargs,
            config={"patterns": Compiler.as_dicts([color.COLOR])},
        )

    def dates(self, name="date", **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name=name,
            **kwargs,
            config={"patterns": Compiler.as_dicts([date_.DATE, date_.MISSING_DAY])},
        )

    def habitats(self, name="habitat", **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name=name,
            **kwargs,
            config={"patterns": Compiler.as_dicts([habitat.HABITAT])},
        )

    def lat_longs(self, name="lat_long", **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name=name,
            **kwargs,
            config={"patterns": Compiler.as_dicts([lat_long.LAT_LONG])},
        )

    def delete_traits(self, traits, **kwargs):
        self.nlp.add_pipe(DELETE_TRAITS, **kwargs, config={"delete": traits})

    def merge(self, **kwargs):
        self.nlp.add_pipe(MERGE_TRAITS, **kwargs)

    def debug_ents(self, **kwargs):
        debug.ents(self.nlp, **kwargs)

    def debug_tokens(self, **kwargs):
        debug.tokens(self.nlp, **kwargs)
