import csv
from pathlib import Path
from typing import Any
from typing import Iterable


def term_data(csv_path: Path, field: str, type_=None) -> dict[str, Any]:
    type_ = type_ if type_ else str
    data = {}
    with open(csv_path) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            value = row.get(field)
            if value not in (None, ""):
                data[row["pattern"]] = type_(value)
    return data


def get_labels(csv_paths: Path | Iterable[Path]) -> list[str]:
    csv_paths = csv_paths if isinstance(csv_paths, Iterable) else [csv_paths]
    labels_ = set()
    for path in csv_paths:
        with open(path) as csv_file:
            reader = csv.DictReader(csv_file)
            labels_ |= {r["label"] for r in reader if r["label"]}
    return sorted(labels_)


def labels_to_remove(
    csv_paths: Path | Iterable[Path], *, keep: str | Iterable[str]
) -> list[str]:
    keep = keep if isinstance(keep, Iterable) else [keep]
    labels_ = [lb for lb in get_labels(csv_paths) if lb not in keep]
    return labels_
