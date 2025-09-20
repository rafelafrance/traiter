import csv
from collections.abc import Iterable
from io import TextIOWrapper
from pathlib import Path
from typing import Any
from zipfile import ZipFile


def look_up_table(
    csv_path: Path | Iterable[Path],
    field: str,
    type_: type | None = None,
) -> dict[str, Any]:
    paths = csv_path if isinstance(csv_path, Iterable) else [csv_path]
    data = {}
    for path in paths:
        terms = read_terms(path)
        data |= term_patterns(terms, field, type_)
    return data


def term_patterns(
    terms: list[dict[str, Any]],
    field: str,
    type_: type | None = None,
) -> dict[str, Any]:
    type_ = type_ if type_ else str
    data = {}
    for term in terms:
        value = term.get(field)
        if value not in (None, ""):
            data[term["pattern"]] = type_(value)
    return data


def read_terms(csv_path: Path | Iterable[Path]) -> list[dict]:
    paths = csv_path if isinstance(csv_path, Iterable) else [csv_path]
    terms = []
    for path in paths:
        if path.suffix == ".zip":
            with ZipFile(path) as zippy, zippy.open(f"{path.stem}.csv") as in_csv:
                reader = csv.DictReader(TextIOWrapper(in_csv, "utf-8"))
                terms += list(reader)
        else:
            with path.open(encoding="utf8") as term_file:
                reader = csv.DictReader(term_file)
                terms += list(reader)
    return terms
