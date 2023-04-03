import csv
from pathlib import Path
from typing import Iterable

from spacy import Language

from ..pipes import debug
from ..pipes import delete
from ..pipes import link
from ..pipes import term_update
from traiter.pylib.traits.pattern_compiler import Compiler


def term_pipe(
    nlp,
    *,
    name: str,
    path: Path | list[Path] = None,
    overwrite_ents=False,
    validate=True,
    **kwargs,
) -> str:
    # Gather the terms
    csv_paths = path if isinstance(path, Iterable) else [path]
    lower, text = [], []
    for path in csv_paths:
        with open(path) as term_file:
            reader = csv.DictReader(term_file)
            terms = list(reader)
            for term in terms:
                pattern = {
                    "label": term["label"],
                    "pattern": term["pattern"],
                }
                if term.get("attr", "lower") == "lower":
                    lower.append(pattern)
                else:
                    text.append(pattern)

    prev = ""

    # Add lower case matches to a phrase pipe
    config = {
        "validate": validate,
        "overwrite_ents": overwrite_ents,
        "phrase_matcher_attr": "LOWER",
    }
    if lower:
        name = f"{name}_lower"
        ruler = nlp.add_pipe("entity_ruler", name=name, config=config, **kwargs)
        ruler.add_patterns(lower)
        prev = name

    # Add exact text matches to a phrase pipe
    config["phrase_matcher_attr"] = "TEXT"
    if text:
        name = name.replace("_lower", "_text")
        kwargs = kwargs if not prev else {"after": prev}
        ruler = nlp.add_pipe("entity_ruler", name=name, config=config, **kwargs)
        ruler.add_patterns(text)
        prev = name

    # Add a pipe for updating the term
    name = f"{name}_update"
    config = {"overwrite": overwrite_ents}
    nlp.add_pipe(term_update.TERM_UPDATE, name=name, config=config, after=prev)
    return name


def ruler_pipe(
    nlp,
    *,
    name: str,
    compiler: Compiler | list[Compiler],
    attr=None,
    overwrite_ents=False,
    validate=True,
    **kwargs,
) -> str:
    compilers = compiler if isinstance(compiler, Iterable) else [compiler]
    patterns = []
    for compiler in compilers:
        compiler.compile()
        for pattern in compiler.patterns:
            patterns.append(
                {"label": compiler.label, "pattern": pattern, "id": compiler.id}
            )
    config = {
        "validate": validate,
        "overwrite_ents": overwrite_ents,
        "phrase_matcher_attr": attr,
    }
    ruler = nlp.add_pipe("entity_ruler", name=name, config=config, **kwargs)
    ruler.add_patterns(patterns)
    return name


def cleanup_pipe(nlp: Language, *, name: str, remove: list[str], **kwargs) -> str:
    nlp.add_pipe(delete.DELETE_TRAITS, name=name, config={"delete": remove}, **kwargs)
    return name


def custom_pipe(nlp: Language, name: str, config: dict, **kwargs):
    nlp.add_pipe(name, config=config, **kwargs)
    return name


def debug_tokens(nlp: Language, **kwargs) -> str:
    return debug.tokens(nlp, **kwargs)


def debug_ents(nlp: Language, **kwargs) -> str:
    return debug.ents(nlp, **kwargs)


def link_pipe(
    nlp,
    *,
    compiler,
    name,
    parents,
    children,
    weights=None,
    reverse_weights=None,
    max_links=None,
    differ=None,
    **kwargs,
) -> str:
    patterns = []
    compiler.compile()
    for pattern in compiler.patterns:
        patterns.append(
            {"label": compiler.label, "pattern": pattern, "id": compiler.id}
        )
    config = {
        "patterns": patterns,
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
    nlp.add_pipe(link.LINK_TRAITS, name=name, config=config, **kwargs)
    return name
