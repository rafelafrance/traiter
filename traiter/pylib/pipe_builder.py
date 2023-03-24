import spacy
from spacy.lang.en import English

from .pattern_compilers.matcher import Compiler
from .patterns import colors
from .patterns import dates
from .patterns import elevations
from .patterns import habitats
from .patterns import lat_longs
from .pipes import debug
from .pipes.add import ADD_TRAITS
from .pipes.delete import DELETE_TRAITS
from .pipes.link import LINK_TRAITS
from .pipes.sentence import SENTENCES
from .pipes.term import TERM_PIPE


class PipeBuilder:
    def __init__(self, base_model="en_core_web_sm", exclude=None):
        exclude = exclude if exclude is not None else []
        exclude = exclude if isinstance(exclude, list) else [exclude]
        self.base_model = base_model
        if base_model.lower() == "english":
            self.nlp = English()
        else:
            self.nlp = spacy.load(base_model, exclude=exclude)
        self.spacy_ent_labels = self.nlp.meta["labels"].get("ner", [])

    def __call__(self, text):
        return self.nlp(text)

    def add_terms(
        self, terms, name=TERM_PIPE, replace=None, merge=False, **kwargs
    ) -> str:
        replace = replace if replace else {}
        self.nlp.add_pipe(
            TERM_PIPE,
            name=name,
            config={"terms": terms.terms, "replace": replace},
            **kwargs,
        )
        if merge:
            return self.merge_entities(name=f"{name}_merge", after=name)
        return name

    def add_traits(self, patterns, name, merge=False, **kwargs) -> str:
        patterns = [p.compile() for p in patterns]
        self.nlp.add_pipe(
            ADD_TRAITS,
            name=name,
            config={"patterns": Compiler.as_dicts(patterns)},
            **kwargs,
        )
        if merge:
            return self.merge_entities(name=f"{name}_merge", after=name)
        return name

    def merge_entities(self, name, **kwargs) -> str:
        self.nlp.add_pipe("merge_entities", name=name, **kwargs)
        return name

    def delete_traits(
        self, name, delete=None, keep=None, delete_when=None, **kwargs
    ) -> str:
        config = {}
        if keep is not None:
            config["keep"] = keep
        if delete is not None:
            config["delete"] = delete
        if delete_when is not None:
            config["delete_when"] = delete_when
        self.nlp.add_pipe(DELETE_TRAITS, name=name, config=config, **kwargs)
        return name

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
        self.nlp.add_pipe(LINK_TRAITS, name=name, config=config, **kwargs)
        return name

    def sentences(self, name=SENTENCES, **kwargs):
        if "parser" in self.nlp.pipe_names:
            self.nlp.remove_pipe("parser")
        self.nlp.add_pipe(
            SENTENCES, name=name, config={"base_model": self.base_model}, **kwargs
        )
        return name

    def colors(self, **kwargs) -> str:
        return self.add_traits([colors.COLORS], name="colors", **kwargs)

    def dates(self, **kwargs) -> str:
        return self.add_traits(
            [dates.DATES, dates.MISSING_DAYS], name="dates", **kwargs
        )

    def elevations(self, **kwargs) -> str:
        return self.add_traits(
            [elevations.ELEVATIONS, elevations.ELEVATION_RANGES],
            name="elevations",
            **kwargs,
        )

    def habitats(self, **kwargs) -> str:
        return self.add_traits(
            [habitats.HABITATS, habitats.NOT_HABITATS], name="habitats", **kwargs
        )

    def lat_longs(self, **kwargs) -> str:
        prev = self.add_traits(
            [lat_longs.LAT_LONGS], name="lat_longs", merge=True, **kwargs
        )
        return self.add_traits(
            [lat_longs.LAT_LONG_UNCERTAIN],
            name="lat_long_uncertain",
            after=prev,
            **kwargs,
        )

    def debug_ents(self, **kwargs) -> str:
        return debug.ents(self.nlp, **kwargs)

    def debug_tokens(self, **kwargs) -> str:
        return debug.tokens(self.nlp, **kwargs)
