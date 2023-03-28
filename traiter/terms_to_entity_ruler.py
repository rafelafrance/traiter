#!/usr/bin/env python3
import argparse
import csv
import shutil
import textwrap
from pathlib import Path

from pylib import log
from spacy.lang.en import English


def main():
    log.started()

    args = parse_args()

    for path in args.traits_dir.glob("**/*.csv"):
        with open(path) as term_file:
            reader = csv.DictReader(term_file)
            terms = list(reader)

        lower = []
        text = []
        for term in terms:
            pattern = {
                "label": term["label"],
                "pattern": term["pattern"],
            }
            if term.get("attr", "lower") == "lower":
                lower.append(pattern)
            else:
                text.append(pattern)

        dir_ = args.traits_dir / path.stem

        if lower:
            nlp = English()
            ruler = nlp.add_pipe("entity_ruler")
            ruler.add_patterns(lower)
            ruler.to_disk(dir_ / f"{path.stem}_terms_lower.jsonl")

        if text:
            nlp = English()
            ruler = nlp.add_pipe("entity_ruler")
            ruler.add_patterns(text)
            ruler.to_disk(dir_ / f"{path.stem}_terms_text.jsonl")

    log.finished()


def parse_args() -> argparse.Namespace:
    description = """Convert terms lists into entity ruler patterns."""

    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--traits-dir",
        type=Path,
        metavar="PATH",
        required=True,
        help="""Holds CSV input files and JSONL output files.""",
    )

    return arg_parser.parse_args()


if __name__ == "__main__":
    main()
