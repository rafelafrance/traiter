from collections import defaultdict
from pathlib import Path
from typing import Iterable

from spacy.language import Language

from .pattern_compiler import ACCUMULATOR
from .pattern_compiler import Compiler
from .trait_util import read_terms
from traiter.pylib.pipes import add
from traiter.pylib.pipes import cleanup
from traiter.pylib.pipes import debug
from traiter.pylib.pipes import link
from traiter.pylib.pipes import phrase
from traiter.pylib.pipes.merge_selected import MERGE_SELECTED


def term_pipe(
    nlp,
    *,
    name: str,
    path: Path | list[Path],
    default_labels: dict[str, str] | None = None,
    **kwargs,
) -> str:
    default_labels = default_labels if default_labels else {}
    paths = path if isinstance(path, Iterable) else [path]

    # Gather terms and make sure they have the needed fields
    by_attr = defaultdict(list)
    replaces = defaultdict(dict)

    for path in paths:
        terms = read_terms(path)
        for term in terms:
            label = term.get("label", default_labels.get(path.stem))
            pattern = {"label": label, "pattern": term["pattern"]}
            attr = term.get("attr", "lower").upper()
            by_attr[attr].append(pattern)
            if replace := term.get("replace"):
                replaces[attr][term["pattern"]] = replace

    # Add a pipe for each phrase matcher attribute
    prev = ""
    base_name = name

    for attr, patterns in by_attr.items():
        name = f"{base_name}_{attr.lower()}"
        config = {
            "patterns": patterns,
            "replace": replaces[attr],
            "attr": attr,
        }
        kwargs = kwargs if not prev else {"after": prev}
        nlp.add_pipe(phrase.PHRASE_PIPE, name=name, config=config, **kwargs)
        prev = name

    return name


def trait_pipe(
    nlp,
    *,
    name: str,
    compiler: list[Compiler] | Compiler,
    keep: list[str] | None = None,
    overwrite: list[str] | None = None,
    merge: list[str] | None = None,
    **kwargs,
) -> str:
    compilers = compiler if isinstance(compiler, Iterable) else [compiler]
    merge = merge if merge else []
    patterns = defaultdict(list)
    dispatch = {}
    relabel = {}

    for comp in compilers:
        comp.compile()
        patterns[comp.label] += comp.patterns

        if comp.on_match:
            dispatch[comp.label] = comp.on_match

        if comp.id:
            relabel[comp.label] = comp.id

    config = {
        "patterns": patterns,
        "dispatch": dispatch,
        "relabel": relabel,
        "keep": keep,
        "overwrite": overwrite,
    }
    nlp.add_pipe(add.ADD_TRAITS, name=name, config=config, **kwargs)

    if merge:
        prev = name
        name = f"{name}_merge"
        config = {"labels": merge}
        nlp.add_pipe(MERGE_SELECTED, name=name, config=config, after=prev)

    return name


def cleanup_pipe(nlp: Language, *, name: str, delete=None, **kwargs) -> str:
    if delete:
        delete = delete if isinstance(delete, list) else [delete]
        ACCUMULATOR.delete(delete)

    config = {"keep": ACCUMULATOR.keep}
    nlp.add_pipe(cleanup.CLEANUP_TRAITS, name=name, config=config, **kwargs)

    return name


def custom_pipe(
    nlp: Language, registered: str, name: str = "", config: dict | None = None, **kwargs
):
    config = config if config else {}
    name = name if name else registered
    nlp.add_pipe(registered, name=name, config=config, **kwargs)
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
