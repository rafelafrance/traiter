"""Get terms from CSV files."""
import csv
from pathlib import Path
from typing import Union

from . import terms
from .. import const

# This points to the traiter vocabulary files
SHARED_CSV = list(const.VOCAB_DIR.glob("*.csv"))


class Csv(terms.Terms):
    """A dictionary of terms."""

    @classmethod
    def read_csv(cls, path: Union[str, Path]) -> "Csv":
        """Read a CSV file."""
        terms_ = cls()

        with open(path) as term_file:
            reader = csv.DictReader(term_file)
            new_terms = list(reader)

        for term in new_terms:
            if not term.get("attr"):
                term["attr"] = "lower"

        terms_ += cls(terms=new_terms)

        return terms_

    @classmethod
    def shared(cls, names: terms.StrList) -> "Csv":
        """Get the contents of a shared vocabulary file."""
        names = names.split() if isinstance(names, str) else names

        terms_ = cls()

        for name in names:

            path_set = {s for s in SHARED_CSV if s.name.lower().startswith(name)}

            if not path_set:
                err = f'\nShared terms "{name}" not found in: '
                err += " ".join(f'"{s.stem}"' for s in SHARED_CSV)
                raise Exception(err)

            path = path_set.pop()

            terms_ += cls.read_csv(path)

        return terms_
