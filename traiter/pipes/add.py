from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path

from spacy.language import Language

from traiter.pipes import cleanup, context, debug, phrase, trait
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import ACCUMULATOR, Compiler


def term_pipe(
    nlp,
    *,
    name: str,
    path: Path | list[Path],
    default_labels: dict[str, str] | None = None,
    delete_patterns: list[str] | str | None = None,
):
    default_labels = default_labels if default_labels else {}
    paths = path if isinstance(path, Iterable) else [path]
    if isinstance(delete_patterns, str):
        delete_patterns = delete_patterns.split()
    delete_patterns = delete_patterns if delete_patterns else []

    # Gather terms and make sure they have the needed fields
    by_attr = defaultdict(list)
    replaces = defaultdict(dict)

    for path_ in paths:
        terms = term_util.read_terms(path_)
        for term in terms:
            if term["pattern"] in delete_patterns:
                continue
            label = term.get("label", default_labels.get(path_.stem))
            pattern = {"label": label, "pattern": term["pattern"]}
            attr = term.get("attr", "lower").upper()
            by_attr[attr].append(pattern)
            if replace := term.get("replace"):
                replaces[attr][term["pattern"]] = replace

    # Add a pipe for each phrase matcher attribute
    with nlp.select_pipes(enable="tokenizer"):
        for attr, patterns in by_attr.items():
            name = f"{name}_{attr.lower()}"
            config = {
                "patterns": patterns,
                "replace": replaces[attr],
                "attr": attr,
            }
            nlp.add_pipe(phrase.PHRASE_PIPE, name=name, config=config)


def trait_pipe(
    nlp,
    *,
    name: str,
    compiler: list[Compiler] | Compiler,
    overwrite: list[str] | None = None,
):
    compilers = compiler if isinstance(compiler, Iterable) else [compiler]
    patterns = defaultdict(list)
    dispatch = {}

    for compiler_ in compilers:
        compiler_.compile()
        patterns[compiler_.label] += compiler_.patterns

        if compiler_.on_match:
            dispatch[compiler_.label] = compiler_.on_match

    config = {
        "patterns": patterns,
        "dispatch": dispatch,
        "keep": ACCUMULATOR.keep,
        "overwrite": overwrite,
    }
    nlp.add_pipe(trait.ADD_TRAITS, name=name, config=config)


def context_pipe(
    nlp,
    *,
    name: str,
    compiler: list[Compiler] | Compiler,
    overwrite: list[str] | None = None,
):
    compilers = compiler if isinstance(compiler, Iterable) else [compiler]
    patterns = defaultdict(list)
    dispatch = {}

    for compiler_ in compilers:
        compiler_.compile()
        patterns[compiler_.label] += compiler_.patterns

        if compiler_.on_match:
            dispatch[compiler_.label] = compiler_.on_match

    config = {
        "patterns": patterns,
        "dispatch": dispatch,
        "overwrite": overwrite,
    }
    nlp.add_pipe(context.CONTEXT_TRAITS, name=name, config=config)


def cleanup_pipe(nlp: Language, *, name: str):
    config = {"keep": ACCUMULATOR.keep}
    nlp.add_pipe(cleanup.CLEANUP_TRAITS, name=name, config=config)


def debug_tokens(nlp: Language):
    debug.tokens(nlp)


def debug_ents(nlp: Language):
    debug.ents(nlp)
