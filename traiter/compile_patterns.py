#!/usr/bin/env python3
import argparse
import textwrap
from dataclasses import dataclass
from pathlib import Path

from pylib import log
from pylib.traits.color import color_compilers as color
from pylib.traits.date import date_compilers as dates
from pylib.traits.elevation import elevation_compilers as elevation
from pylib.traits.habitat import habitat_compilers as habitat
from pylib.traits.lat_long import lat_long_compilers as lat_long
from spacy.lang.en import English


@dataclass
class Matchers:
    name: str
    dir: str
    matchers: list


def main():
    log.started()

    all_matchers = [
        Matchers("color", "color", [color.COLOR]),
        Matchers("date", "date", [dates.DATE, dates.MISSING_DAYS]),
        Matchers(
            "elevation", "elevation", [elevation.ELEVATION, elevation.ELEVATION_RANGE]
        ),
        Matchers("habitat", "habitat", [habitat.HABITATS, habitat.NOT_HABITATS]),
        Matchers("lat_long", "lat_long", [lat_long.LAT_LONG]),
        Matchers("lat_long_uncertain", "lat_long", [lat_long.LAT_LONG_UNCERTAIN]),
    ]

    args = parse_args()

    for matchers in all_matchers:
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

    return arg_parser.parse_args()


if __name__ == "__main__":
    main()
