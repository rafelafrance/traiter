#!/usr/bin/env python3
import argparse
import csv
import json
import shutil
import textwrap
from pathlib import Path

from pylib import log
from spacy.lang.en import English


def main():
    log.started()

    args = parse_args()

    for path in args.term_dir.glob("*.csv"):
        with open(path) as term_file:
            reader = csv.DictReader(term_file)
            terms = list(reader)

        lower = []
        text = []
        data = []
        for term in terms:
            pattern = {
                "label": term["label"],
                "pattern": term["pattern"],
            }
            if term.get("replace"):
                pattern["id"] = term["replace"]
            if term.get("attr", "lower") == "lower":
                lower.append(pattern)
            else:
                text.append(pattern)

            headers = [k for k in term.keys() if k not in ["label", "replace", "attr"]]
            if len(headers) > 1:
                datum = {h: term[h] for h in headers if term[h]}
                if len(datum) > 1:
                    data.append(datum)

        stem = path.stem
        stem = stem[:-1] if stem[-1] == "s" and stem[-2] != "s" else stem
        dir_ = args.rules_dir / stem

        dir_.mkdir(exist_ok=True)
        shutil.copy(path, dir_ / f"{stem}.csv")
        with open(dir_ / "__init__.py", "w") as out_file:
            out_file.write("")

        if lower:
            nlp = English()
            ruler = nlp.add_pipe("entity_ruler")
            ruler.add_patterns(lower)
            ruler.to_disk(dir_ / f"{stem}_terms_lower.jsonl")

        if text:
            nlp = English()
            ruler = nlp.add_pipe("entity_ruler")
            ruler.add_patterns(text)
            ruler.to_disk(dir_ / f"{stem}_terms_text.jsonl")

        if data:
            with open(dir_ / f"{stem}_data.jsonl", "w") as out_file:
                for datum in data:
                    line = json.dumps(datum)
                    out_file.write(line)
                    out_file.write("\n")

    log.finished()


def parse_args() -> argparse.Namespace:
    description = """Convert terms lists into entity ruler patterns."""

    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--term-dir",
        type=Path,
        metavar="PATH",
        required=True,
        help="""Get the terms from the CSV files in this directory.""",
    )

    arg_parser.add_argument(
        "--rules-dir",
        type=Path,
        metavar="PATH",
        required=True,
        help="""Save the term JSONL files to this directory.""",
    )

    return arg_parser.parse_args()


if __name__ == "__main__":
    main()
