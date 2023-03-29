from pathlib import Path

from spacy import Language

from .pipes import debug
from .pipes import delete
from .pipes import link
from .pipes import term_update


def term_pipe(
    nlp,
    *,
    name: str,
    path: Path,
    attr=None,
    overwrite_ents=False,
    validate=True,
    **kwargs,
) -> str:
    config = {
        "validate": validate,
        "overwrite_ents": overwrite_ents,
        "phrase_matcher_attr": attr,
    }
    nlp.add_pipe("entity_ruler", name=name, config=config, **kwargs).from_disk(path)
    update_name = f"{name}_update"
    nlp.add_pipe(term_update.TERM_UPDATE, name=update_name, after=name)
    return update_name


def ruler_pipe(
    nlp,
    *,
    name: str,
    path: Path,
    attr=None,
    overwrite_ents=False,
    validate=True,
    **kwargs,
) -> str:
    config = {
        "validate": validate,
        "overwrite_ents": overwrite_ents,
        "phrase_matcher_attr": attr,
    }
    nlp.add_pipe("entity_ruler", name=name, config=config, **kwargs).from_disk(path)
    return name


def cleanup_pipe(nlp: Language, *, name: str, remove: list[str], **kwargs) -> str:
    nlp.add_pipe(delete.DELETE_TRAITS, name=name, config={"delete": remove}, **kwargs)
    return name


def data_pipe(nlp: Language, name: str, **kwargs) -> str:
    nlp.add_pipe(name, **kwargs)
    return name


def debug_tokens(nlp: Language, message: str = "", **kwargs) -> str:
    return debug.tokens(nlp, message, **kwargs)


def debug_ents(nlp: Language, message: str = "", **kwargs) -> str:
    return debug.ents(nlp, message, **kwargs)


def link_pipe(
    nlp,
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
