import csv
from io import TextIOWrapper
from pathlib import Path
from typing import Any
from typing import Iterable
from zipfile import ZipFile


def term_data(
    csv_path: Path | Iterable[Path], field: str, type_=None
) -> dict[str, Any]:
    paths = csv_path if isinstance(csv_path, Iterable) else [csv_path]
    type_ = type_ if type_ else str
    data = {}
    for path in paths:
        with open(path) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                value = row.get(field)
                if value not in (None, ""):
                    data[row["pattern"]] = type_(value)
    return data


def get_labels(csv_paths: Path | Iterable[Path]) -> list[str]:
    csv_paths = csv_paths if isinstance(csv_paths, Iterable) else [csv_paths]
    labels = set()
    for path in csv_paths:
        terms = read_terms(path)
        try:
            labels |= {t["label"] for t in terms}
        except KeyError:
            labels.add(path.stem)
    return sorted(labels)


def labels_to_remove(
    csv_paths: Path | Iterable[Path], *, keep: str | Iterable[str]
) -> list[str]:
    keep = keep if isinstance(keep, Iterable) else [keep]
    labels = [lb for lb in get_labels(csv_paths) if lb not in keep]
    return labels


def read_terms(csv_path: Path | Iterable[Path]):
    paths = csv_path if isinstance(csv_path, Iterable) else [csv_path]
    for path in paths:
        if path.suffix == ".zip":
            with ZipFile(path) as zippy:
                with zippy.open(f"{path.stem}.csv") as in_csv:
                    reader = csv.DictReader(TextIOWrapper(in_csv, "utf-8"))
                    terms = list(reader)
        else:
            with open(path) as term_file:
                reader = csv.DictReader(term_file)
                terms = list(reader)
    return terms
