import spacy

from .pattern_compilers.matcher import Compiler
from .patterns import color
from .patterns import date_
from .patterns import habitat
from .patterns import lat_long
from .pipes import debug
from .pipes.add import ADD_TRAITS
from .pipes.delete import DELETE_TRAITS
from .pipes.link import LINK_TRAITS
from .pipes.sentence import SENTENCES
from .pipes.term import TERM_PIPE


class PipelineBuilder:
    def __init__(self, base_model="en_core_web_sm", exclude=None):
        exclude = exclude if exclude is not None else []
        exclude = exclude if isinstance(exclude, list) else [exclude]
        self.base_model = base_model
        self.nlp = spacy.load(base_model, exclude=exclude)
        self.spacy_ent_labels = self.nlp.meta["labels"].get("ner", [])

    def __call__(self, text):
        return self.nlp(text)

    def add_terms(self, terms, name=TERM_PIPE, replace=None, merge=False, **kwargs):
        replace = replace if replace else {}
        self.nlp.add_pipe(
            TERM_PIPE,
            name=name,
            config={"terms": terms.data, "replace": replace},
            **kwargs,
        )
        if merge:
            self.merge_entities(name=f"{name}_merge", after=name)

    def add_traits(self, patterns, name, merge=False, **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name=name,
            config={"patterns": Compiler.as_dicts(patterns)},
            **kwargs,
        )
        if merge:
            self.merge_entities(name=f"{name}_merge", after=name)

    def merge_entities(self, name, **kwargs):
        self.nlp.add_pipe("merge_entities", name=name, **kwargs)

    def delete_traits(self, name, delete=None, delete_when=None, **kwargs):
        config = {}
        if delete is not None:
            config["delete"] = delete
        if delete_when is not None:
            config["delete_when"] = delete_when
        self.nlp.add_pipe(DELETE_TRAITS, name=name, config=config, **kwargs)

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

    def add_links(
        self,
        patterns,
        name,
        parents,
        children,
        weights=None,
        reverse_weights=None,
        max_links=None,
        differ=None,
        **kwargs,
    ):
        config = {
            "patterns": Compiler.as_dicts(patterns),
            "parents": parents,
            "children": children,
        }
        if weights is not None:
            config["weights"] = weights
        if reverse_weights is not None:
            config["reverse_weights"] = reverse_weights
        if max_links is not None:
            config["max_links"] = max_links
        if differ is not None:
            config["differ"] = differ
        self.nlp.add_pipe(LINK_TRAITS, name=name, config=config, **kwargs)

    def sentences(self, **kwargs):
        if "parser" in self.nlp.pipe_names:
            self.nlp.remove_pipe("parser")
        self.nlp.add_pipe(SENTENCES, config={"base_model": self.base_model}, **kwargs)

    def colors(self, **kwargs):
        self.add_traits([color.COLOR], name="colors", **kwargs)

    def dates(self, **kwargs):
        self.add_traits([date_.DATE, date_.MISSING_DAY], name="dates", **kwargs)

    def habitats(self, **kwargs):
        self.add_traits([habitat.HABITAT], name="habitats", **kwargs)

    def lat_longs(self, **kwargs):
        self.add_traits([lat_long.LAT_LONG], name="lat_longs", **kwargs)

    def debug_ents(self, **kwargs):
        debug.ents(self.nlp, **kwargs)

    def debug_tokens(self, **kwargs):
        debug.tokens(self.nlp, **kwargs)
