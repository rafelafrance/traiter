#!/usr/bin/env python3
import argparse
import textwrap
from pathlib import Path

from pylib import log
from pylib.new_patterns.color import color_compilers as color
from pylib.new_patterns.date import date_compilers as dates
from pylib.patterns import elevations
from pylib.patterns import habitats
from pylib.patterns import lat_longs
from spacy.lang.en import English


def main():
    log.started()

    all_matchers = {
        "color": {"dir": "color", "matchers": [color.COLORS]},
        "date": {"dir": "date", "matchers": [dates.DATES, dates.MISSING_DAYS]},
        "elevation": {
            "dir": "elevation",
            "matchers": [elevations.ELEVATIONS, elevations.ELEVATION_RANGES],
        },
        "habitat": {
            "dir": "habitat",
            "matchers": [habitats.HABITATS, habitats.NOT_HABITATS],
        },
        "lat_long": {"dir": "lat_long", "matchers": [lat_longs.LAT_LONGS]},
        "lat_long_uncertain": {
            "dir": "lat_long",
            "matchers": [lat_longs.LAT_LONG_UNCERTAIN],
        },
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
