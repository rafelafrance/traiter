import csv
from collections.abc import Iterable
from io import TextIOWrapper
from pathlib import Path
from typing import Any
from zipfile import ZipFile


def look_up_table(
    csv_path: Path | Iterable[Path],
    field: str,
    type_: str | None = None,
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
    type_: str | None = None,
) -> dict[str, Any]:
    type_ = type_ if type_ else str
    data = {}
    for term in terms:
        value = term.get(field)
        if value not in (None, ""):
            data[term["pattern"]] = type_(value)
    return data


def get_labels(
    csv_paths: Path | Iterable[Path],
    default_labels: dict[str, str] | None = None,
) -> list[str]:
    csv_paths = csv_paths if isinstance(csv_paths, Iterable) else [csv_paths]
    default_labels = default_labels if default_labels else {}
    labels = set()
    for path in csv_paths:
        terms = read_terms(path)
        try:
            labels |= {t["label"] for t in terms}
        except KeyError:
            if label := default_labels.get(path.stem):
                labels.add(label)
    return sorted(labels)


def delete_terms(terms: list, patterns: list[str] | str) -> list:
    patterns = patterns if isinstance(patterns, list) else patterns.split()
    terms = [t for t in terms if t["pattern"] not in patterns]
    return terms


def filter_labels(terms: list, keep: list[str] | str) -> list:
    keep = keep if isinstance(keep, list) else keep.split()
    terms = [t for t in terms if t["label"] in keep]
    return terms


def labels_to_remove(
    csv_paths: Path | Iterable[Path],
    *,
    keep: str | Iterable[str] | None = None,
) -> list[str]:
    labels = get_labels(csv_paths)
    if keep:
        keep = keep if isinstance(keep, Iterable) else [keep]
        labels = [lb for lb in labels if lb not in keep]
    return labels


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
