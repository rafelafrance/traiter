from collections import defaultdict
from pathlib import Path
from typing import Iterable

from spacy import Language

from .pattern_compiler import Compiler
from .trait_util import read_terms
from traiter.pipes import add
from traiter.pipes import debug
from traiter.pipes import delete
from traiter.pipes import link
from traiter.pipes import phrase
from traiter.pipes.merge_selected import MERGE_SELECTED


def term_pipe(
    nlp,
    *,
    name: str,
    path: Path | list[Path] = None,
    default_labels: dict[str, str] = None,
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
    compiler: Compiler | list[Compiler],
    keep: list[str] = None,
    overwrite: list[str] = None,
    merge: list[str] = None,
    **kwargs,
) -> str:
    compilers = compiler if isinstance(compiler, Iterable) else [compiler]
    merge = merge if merge else []
    patterns = defaultdict(list)
    dispatch = {}
    relabel = {}

    for compiler in compilers:
        compiler.compile()
        patterns[compiler.label] += compiler.patterns

        if compiler.on_match:
            dispatch[compiler.label] = compiler.on_match

        if compiler.id:
            relabel[compiler.label] = compiler.id

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


def cleanup_pipe(nlp: Language, *, name: str, remove: list[str], **kwargs) -> str:
    nlp.add_pipe(delete.DELETE_TRAITS, name=name, config={"delete": remove}, **kwargs)
    return name


def custom_pipe(
    nlp: Language, registered: str, name: str = "", config: dict = None, **kwargs
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
