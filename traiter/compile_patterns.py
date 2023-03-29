#!/usr/bin/env python3
import argparse
import logging
import textwrap
from pathlib import Path

from pylib import log
from pylib.traits.color import color_compilers as color
from pylib.traits.date import date_compilers as dates
from pylib.traits.elevation import elevation_compilers as elevation
from pylib.traits.habitat import habitat_compilers as habitat
from pylib.traits.lat_long import lat_long_compilers as lat_long
from spacy.lang.en import English


class Matchers:
    def __init__(self, name, matchers, dir_=None):
        self.name = name
        self.matchers = matchers if isinstance(matchers, list) else [matchers]
        self.dir = dir_ if dir_ else name


def main():
    log.started()

    all_matchers = [
        Matchers("color", color.COMPILERS),
        Matchers("date", dates.COMPILERS),
        Matchers("elevation", elevation.COMPILERS),
        Matchers("habitat", habitat.COMPILERS),
        # We want to break these out in to separate pattern sets
        Matchers("lat_long", [lat_long.LAT_LONG]),
        Matchers("lat_long_uncertain", [lat_long.LAT_LONG_UNCERTAIN], "lat_long"),
    ]

    args = parse_args()

    for matchers in all_matchers:
        if args.trait and matchers.dir != args.trait:
            continue

        logging.info(f"Compiling {matchers.name}")

        patterns = []
        for matcher in matchers.matchers:
            for pattern in matcher.patterns:
                line = {
                    "label": matcher.label,
                    "pattern": pattern,
                }
                if matcher.id:
                    line["id"] = matcher.id
                patterns.append(line)

        nlp = English()
        ruler = nlp.add_pipe("entity_ruler")
        ruler.add_patterns(patterns)

        dir_ = args.traits_dir / matchers.dir

        path = dir_ / f"{matchers.name}_patterns.jsonl"
        ruler.to_disk(path)

    log.finished()


def parse_args() -> argparse.Namespace:
    description = """Convert pattern objects into entity ruler patterns."""

    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--traits-dir",
        type=Path,
        metavar="PATH",
        required=True,
        help="""Save the term JSONL files to this directory.""",
    )

    arg_parser.add_argument("--trait", help="Only compile patterns for this trait.")

    return arg_parser.parse_args()


if __name__ == "__main__":
    main()
