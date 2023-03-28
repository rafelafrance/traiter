from pathlib import Path

from spacy import Language

from ..pipes import delete


def ruler_pipe(
    nlp,
    *,
    name: str,
    path: Path,
    attr=None,
    overwrite_ents=False,
    validate=True,
    **kwargs,
):
    config = {
        "validate": validate,
        "overwrite_ents": overwrite_ents,
        "phrase_matcher_attr": attr,
    }
    nlp.add_pipe("entity_ruler", name=name, config=config, **kwargs).from_disk(path)
    return name


def cleanup_pipe(nlp: Language, *, name: str, cleanup: list[str], **kwargs):
    nlp.add_pipe(delete.DELETE_TRAITS, name=name, config={"delete": cleanup}, **kwargs)
    return name
