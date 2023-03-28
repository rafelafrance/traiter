#!/usr/bin/env python3
import argparse
import textwrap
from pathlib import Path

from pylib import log
from pylib.traits.color import color_compilers as color
from pylib.traits.date import date_compilers as dates
from pylib.traits.elevation import elevation_compilers as elevation
from pylib.traits.habitat import habitat_compilers as habitat
from pylib.traits.lat_long import lat_long_compilers as lat_long
from spacy.lang.en import English


def main():
    log.started()

    all_matchers = {
        "color": [color.COLOR],
        "date": [dates.DATE, dates.MISSING_DAYS],
        "elevation": [elevation.ELEVATION, elevation.ELEVATION_RANGE],
        "habitat": [habitat.HABITATS, habitat.NOT_HABITATS],
        "lat_long": [lat_long.LAT_LONG],
        "lat_long_uncertain": [lat_long.LAT_LONG_UNCERTAIN],
    }

    args = parse_args()

    for name, data in all_matchers.items():
        patterns = []
        for matcher in data["matchers"]:
            for pattern in matcher.patterns:
                patterns.append(
                    {
                        "label": matcher.label,
                        "pattern": pattern,
                    }
                )

        nlp = English()
        ruler = nlp.add_pipe("entity_ruler")
        ruler.add_patterns(patterns)

        dir_ = args.rules_dir / data["dir"]
        dir_.mkdir(exist_ok=True)

        path = dir_ / f"{name}_patterns.jsonl"
        ruler.to_disk(path)

    log.finished()


def parse_args() -> argparse.Namespace:
    description = """Convert pattern objects into entity ruler patterns."""

    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
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
