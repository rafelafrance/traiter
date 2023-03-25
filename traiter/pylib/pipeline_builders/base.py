from dataclasses import dataclass
from typing import Callable

import spacy
from spacy.lang.en import English

from ..pattern_compilers.matcher import Compiler
from ..pipes.add import ADD_TRAITS
from ..pipes.debug import DEBUG_ENTITIES
from ..pipes.debug import DEBUG_TOKENS
from ..pipes.delete import DELETE_TRAITS
from ..pipes.link import LINK_TRAITS
from ..pipes.sentence import SENTENCES
from ..pipes.term import TERM_PIPE
from ..term_list import TermList


@dataclass
class Pipe:
    func: Callable
    kwargs: dict


class BasePipelineBuilder:
    def __init__(self, *, base_model="en_core_web_sm", exclude=None):
        exclude = exclude if exclude is not None else []
        exclude = [exclude] if isinstance(exclude, str) else exclude
        self.base_model = base_model
        if base_model.lower() == "english":
            self.nlp = English()
        else:
            self.nlp = spacy.load(base_model, exclude=exclude)
        self.spacy_ent_labels = self.nlp.meta["labels"].get("ner", [])
        self.pipeline: list[Pipe] = []
        self.debug_count = 0
        self.patterns = []
        self.traits_without_matcher: list[str] = []

    def __call__(self, text):
        return self.nlp(text)

    def build(self):
        for pipe in self.pipeline:
            pipe.func(**pipe.kwargs)
        return self

    def _add_terms(self, *, name, config, all_terms, **kwargs):
        if all_terms:
            terms = []
            for pat in self.patterns:
                terms += pat.terms
            config["terms"] = terms
        self.nlp.add_pipe(TERM_PIPE, name=name, config=config, **kwargs)

    def _add_traits(self, *, name, config, **kwargs):
        patterns = [p.compile() for p in config["patterns"]]
        config["patterns"] = Compiler.as_dicts(patterns)
        self.nlp.add_pipe(ADD_TRAITS, name=name, config=config, **kwargs)

    def _merge_entities(self, *, name, **kwargs):
        self.nlp.add_pipe("merge_entities", name=name, **kwargs)

    def _delete_traits(self, *, name, config, keep_outputs, **kwargs):
        if keep_outputs:
            keep = config["keep"] if config.get("keep") else []
            keep += self.traits_without_matcher
            for pat in self.patterns:
                if pat.output:
                    keep += pat.output
            config["keep"] = keep
        self.nlp.add_pipe(DELETE_TRAITS, name=name, config=config, **kwargs)

    def _add_links(self, *, name, config, **kwargs):
        self.nlp.add_pipe(LINK_TRAITS, name=name, config=config, **kwargs)

    def _sentences(self, *, name, config, **kwargs):
        if "parser" in self.nlp.pipe_names:
            self.nlp.remove_pipe("parser")
        self.nlp.add_pipe(SENTENCES, name=name, config=config, **kwargs)

    def _debug_ents(self, *, name, **kwargs):
        self.nlp.add_pipe(DEBUG_ENTITIES, name=name, **kwargs)

    def _debug_tokens(self, *, name, **kwargs):
        self.nlp.add_pipe(DEBUG_TOKENS, name=name, **kwargs)

    def add_terms(
        self,
        terms=None,
        *,
        name="terms",
        replace=None,
        merge=False,
        all_terms=False,
        **kwargs,
    ) -> str:
        terms = terms if terms else TermList()
        replace = replace if replace else {}
        config = {"terms": terms.terms, "replace": replace}
        kwargs |= {"name": name, "config": config, "all_terms": all_terms}
        self.pipeline.append(Pipe(self._add_terms, kwargs=kwargs))
        if merge:
            return self.merge_entities(name=f"{name}_merge", after=name)
        return name

    def add_traits(self, patterns, *, name, merge=False, **kwargs) -> str:
        self.patterns += patterns
        config = {"patterns": patterns}
        kwargs |= {"name": name, "config": config}
        self.pipeline.append(Pipe(self._add_traits, kwargs=kwargs))
        if merge:
            return self.merge_entities(name=f"{name}_merge", after=name)
        return name

    def merge_entities(self, *, name, **kwargs) -> str:
        kwargs |= {"name": name}
        self.pipeline.append(Pipe(self._merge_entities, kwargs=kwargs))
        return name

    def delete_traits(
        self,
        name,
        *,
        delete=None,
        keep=None,
        delete_when=None,
        keep_outputs=False,
        **kwargs,
    ) -> str:
        config = {}
        if keep is not None:
            config["keep"] = keep
        if delete is not None:
            config["delete"] = delete
        if delete_when is not None:
            config["delete_when"] = delete_when
        kwargs |= {
            "name": name,
            "config": config,
            "keep_outputs": keep_outputs,
        }
        self.pipeline.append(Pipe(self._delete_traits, kwargs=kwargs))
        return name

    def add_links(
        self,
        patterns,
        *,
        name,
        parents,
        children,
        weights=None,
        reverse_weights=None,
        max_links=None,
        differ=None,
        **kwargs,
    ) -> str:
        patterns = [p.compile() for p in patterns]
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
        kwargs |= {"name": name, "config": config}
        self.pipeline.append(Pipe(self._add_links, kwargs=kwargs))
        return name

    def sentences(self, name=SENTENCES, **kwargs) -> str:
        kwargs |= {"name": name, "config": {"base_model": self.base_model}}
        self.pipeline.append(Pipe(self._sentences, kwargs=kwargs))
        return name

    def debug_ents(self, **kwargs) -> str:
        self.debug_count += 1
        name = f"debug_entities_{self.debug_count}"
        kwargs |= {"name": name, "config": {}}
        self.pipeline.append(Pipe(self._debug_ents, kwargs=kwargs))
        return name

    def debug_tokens(self, **kwargs) -> str:
        self.debug_count += 1
        name = f"debug_tokens_{self.debug_count}"
        kwargs |= {"name": name, "config": {}}
        self.pipeline.append(Pipe(self._debug_tokens, kwargs=kwargs))
        return name
