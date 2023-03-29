import csv
from pathlib import Path
from typing import Any
from typing import Iterable

from .. import const


def term_data(csv_path: Path, field: str, type_=None) -> dict[str, Any]:
    type_ = type_ if type_ else str
    with open(csv_path) as csv_file:
        reader = csv.DictReader(csv_file)
        return {r["pattern"]: type_(r[field]) for r in reader if r.get(field)}


def get_labels(csv_paths: Path | Iterable[Path]) -> list[str]:
    csv_paths = csv_paths if isinstance(csv_paths, Iterable) else [csv_paths]
    labels_ = set()
    for path in csv_paths:
        with open(path) as csv_file:
            reader = csv.DictReader(csv_file)
            labels_ |= {r["label"] for r in reader if r["label"]}
    return sorted(labels_)


def labels_to_remove(
    csv_paths: Path | Iterable[Path], keeps: str | Iterable[str]
) -> list[str]:
    keeps = keeps if isinstance(keeps, Iterable) else [keeps]
    labels_ = [lb for lb in get_labels(csv_paths) if lb not in keeps]
    return labels_
